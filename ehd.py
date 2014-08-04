import wx
import urllib.request, urllib, urllib.parse, http, http.cookiejar, os.path, re, io, html.parser
import threading
import uuid


class EHDownloader(wx.App):

    def OnInit(self):
        frm = GuiWindow("E-Hentai Downloader")
        frm.Show()
        return 1


class GuiWindow(wx.Frame):

    def __init__(self, title):

        wx.Frame.__init__(self, None, -1, title, size=(420, 200), pos=(400, 448))
        panel = wx.Panel(self, wx.ID_ANY)

        self.dm = DownloadCueManager()

        self.url_input = wx.TextCtrl(panel, wx.ID_ANY, 'Gallery URL')
        self.add_button = wx.Button(panel, wx.ID_ANY, 'Add', size=(50, 27))
        self.cue_list = DispCueList(panel, wx.ID_ANY)
        self.start_button = wx.Button(panel, wx.ID_ANY, 'Start')
        self.stop_button = wx.Button(panel, wx.ID_ANY, 'Stop')
        self.stop_button.Disable()

        self.add_button.Bind(wx.EVT_BUTTON, self.click_add_button)
        self.start_button.Bind(wx.EVT_BUTTON, self.click_start_button)
        self.stop_button.Bind(wx.EVT_BUTTON, self.click_stop_button)

        self.Bind(wx.EVT_TIMER, self.watch_cue_list, id=1)
        self.Bind(wx.EVT_TIMER, self.execute_download, id=2)

        self.watcher_thread = wx.Timer(self, id=1)
        self.watcher_thread.Start(1000)

        line1 = wx.BoxSizer(wx.HORIZONTAL)
        line1.Add(self.url_input, proportion=1, flag=wx.GROW)
        line1.Add(self.add_button, proportion=0, flag=wx.ALIGN_RIGHT)

        line2 = wx.BoxSizer(wx.HORIZONTAL)
        line2.Add(self.cue_list, proportion=1, flag=wx.GROW)

        line3 = wx.BoxSizer(wx.HORIZONTAL)
        line3.Add(self.start_button, proportion=0, flag=wx.SHAPED | wx.ALIGN_CENTER)
        line3.Add(self.stop_button, proportion=0, flag=wx.SHAPED | wx.ALIGN_CENTER)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(line1, proportion=0, flag=wx.ALIGN_RIGHT | wx.EXPAND)
        layout.Add((-1, 10))
        layout.Add(line2, proportion=1, flag=wx.GROW)
        layout.Add((-1, 10))
        layout.Add(line3, proportion=0, flag=wx.ALIGN_CENTER)

        panel.SetSizer(layout)

    def click_add_button(self, event):
        got_url = self.url_input.GetValue()
        t = threading.Thread(target=self.dm.add_cue, args=[got_url])
        t.setDaemon(True)
        t.start()
        self.url_input.Clear()

    def click_start_button(self, event):
        self.download_thread = wx.Timer(self, id=2)
        self.download_thread.Start(10000)
        self.stop_button.Enable()
        self.start_button.Disable()

    def click_stop_button(self, event):
        self.download_thread.Stop()
        self.start_button.Enable()
        self.stop_button.Disable()

    def update_cue_list(self):
        self.dm.clean_cue_list()
        cl = self.dm.get_cue_list()
        self.cue_list.DeleteAllItems()
        for i in range(len(cl)):
            self.cue_list.InsertItem(i, i)
            self.cue_list.SetItem(i, 1, cl[i].get_gallery_name())
            self.cue_list.SetItem(i, 2, cl[i].get_status())

    def watch_cue_list(self, event):
        self.update_cue_list()

    def execute_download(self, event):
        self.dm.download()


class DispCueList(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
        self.InsertColumn(0, "#")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Status")

        self.SetColumnWidth(0, 30)
        self.SetColumnWidth(1, 270)
        self.SetColumnWidth(2, 100)


class DownloadCue():

    def __init__(self, gallery_url):
        self.gallery_url = gallery_url
        self.p = UrlParser()
        self.o = UrlOpener()
        self.status = "Waiting"
        self.unique_id = uuid.uuid4()

        self.gallery_name = self.p.get_file_name(self.o.open_page(self.gallery_url))
        self.pre_file_url = urllib.parse.unquote(self.p.phase1(self.o.open_page(self.gallery_url)))
        self.file_url = urllib.parse.unquote(self.p.phase2(self.o.open_page(self.pre_file_url))) + '?start=1'

    def get_unique_id(self):
        return self.unique_id

    def get_file_url(self):
        return self.file_url

    def get_gallery_name(self):
        return self.gallery_name

    def get_status(self):
        return self.status

    def change_status(self, status):
        self.status = status


class DownloadCueManager():

    def __init__(self):
        self.cue_list = []
        self.num_of_downloader = 2
        self.downloader = []
        for i in range(0, self.num_of_downloader):
            self.downloader.append(Downloader())

    def download(self):
        for i in range(0, self.num_of_downloader):
            if self.is_not_empty() and self.downloader[i].get_is_usable():
                t = threading.Thread(target=self.downloader[i].run, args=[self.get_first_cue()])
                t.setDaemon(True)
                t.start()

    def is_not_empty(self):
        return len(self.cue_list) != 0

    def get_cue_list(self):
        return self.cue_list

    def add_cue(self, gallery_url):
        cue = DownloadCue(gallery_url)
        self.cue_list.append(cue)

    def get_first_cue(self):
        cue = self.cue_list[0]
        cue.change_status('Downloading')
        return cue

    def clean_cue_list(self):
        self.cue_list = [x for x in self.cue_list if x.status != "Done"]


class Downloader():

    def __init__(self):
        self.is_usable = True

    def get_is_usable(self):
        return self.is_usable

    def run(self, dc):
        self.is_usable = False
        dc.o.save_file(dc.get_file_url(), dc.get_gallery_name())
        dc.change_status("Done")
        self.is_usable = True


class UrlOpener():

    def __init__(self):

        self.cookiefile = 'cookie.txt'
        self.cj = http.cookiejar.MozillaCookieJar()
        self.useragent = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        if os.path.exists(self.cookiefile):
            self.cj.load(self.cookiefile)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj), urllib.request.HTTPRedirectHandler)
        urllib.request.install_opener(self.opener)

    def open_page(self, fileurl):
        post = {'dlcheck': 'Download Archive'}
        post = urllib.parse.urlencode(post).encode('utf-8')
        html = urllib.request.urlopen(fileurl, post)
        return html

    def save_file(self, fileurl, filename):
        filename = filename + '.zip'
        html = urllib.request.urlopen(fileurl)
        result = open(filename, 'bw')
        result.write(html.read())


class UrlParser(html.parser.HTMLParser):

    def phase1(self, html):
        html_to_parse = io.StringIO(html.read().decode(encoding='utf-8', errors='strict'))
        lines = html_to_parse.readlines()
        for line in lines:
            if "Archive Download" in line:
                print(line)
                a = re.search('\'http([^\']*)\'', line)
                if 'archiver' in a.group():
                    f = a.group()
                    f = f[1:-1]
                    print(f)
        f = f.replace('&amp;', '&')
        return f

    def phase2(self, html):
        html_to_parse = io.StringIO(html.read().decode(encoding='utf-8', errors='strict'))
        lines = html_to_parse.readlines()
        for line in lines:
            if 'document.location' in line:
                a = re.search('\"([^\"])*\"', line)
                h = a.group()
                h = h[1:-1]
        return h

    def get_file_name(self, html):
        html_to_parse = io.StringIO(html.read().decode(encoding='utf-8', errors='strict'))
        lines = html_to_parse.readlines()
        for line in lines:
            if '<title>' in line:
                a = re.search('>([^\"])*<', line)
                n = a.group()
                n = n[1:-1]
        return n


if __name__ == "__main__":
    application = EHDownloader()
    application.MainLoop()
