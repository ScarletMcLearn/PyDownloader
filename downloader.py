from PyQt4.QtCore import *
from PyQt4.QtGui import *
import urllib
import sys

class Downloader(QDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		
		layout = QVBoxLayout()
		
		self.url = QLineEdit()
		self.save_location = QLineEdit()
		self.progress = QProgressBar()
		download = QPushButton("Download")
		browse = QPushButton("Browse")

		self.url.setPlaceholderText("URL")
		self.save_location.setPlaceholderText("File save location")

		self.progress.setValue(0)
		self.progress.setAlignment(Qt.AlignHCenter)

		layout.addWidget(self.url)
		layout.addWidget(self.save_location)
		layout.addWidget(browse)
		layout.addWidget(self.progress)
		layout.addWidget(download)

		self.setLayout(layout)

		self.setWindowTitle("Downloader")
		self.setFocus()

		download.clicked.connect(self.download)
		browse.clicked.connect(self.browse_file)

	def browse_file(self):
		save_file = QFileDialog.getSaveFileName(self, caption="Save file as...", directory=".", filter="All Files (*.*)")
		self.save_location.setText(QDir.toNativeSeparators(save_file))

	def download(self):
		url = str(self.url.text())
		save_location = self.save_location.text()
		try:
			urllib.urlretrieve(url, save_location, self.report)
		except Exception:
			QMessageBox.warning(self, "Warning", "Download failed")
			return

		QMessageBox.information(self, "Success!", "The download is complete")
		self.progress.setValue(0)
		self.url.setText("")
		self.save_location.setText("")

	def report(self, blocknum, blocksize, totalsize):
		readsofar = blocknum * blocksize
		if totalsize > 0:
			percent = readsofar * 100 / totalsize
			self.progress.setValue(int(percent))

app = QApplication(sys.argv)
dl = Downloader()
dl.show()
sys.exit(app.exec_())
