import os
import shutil
import time
import sys
import Tkinter
import tkMessageBox
import tkFileDialog
import threading
from PIL import ImageTk

class DropBox_SYNC():

	def __init__(self, ide_name = "", project_name = "", dropbox_folder = "", fileselect = "", dropboxfile = "", workspace_name = "", backup = True):
		self.ide = ide_name
		self.workspace_name = workspace_name # location that contains smaller projects/folders
		self.project_name = project_name
		self.dropbox_folder = dropbox_folder

		self.localfile = fileselect
		self.dropboxfile = dropboxfile

		self.backup = backup

		self.ide_mode = True # ide mode allows selection of project name + folders

		if "intellij" in self.ide:
			self.ide_dir =  "IdeaProjects"
		else:
			self.ide_dir = workspace_name

		self.localproject = os.path.join(os.environ['USERPROFILE'], self.ide_dir) # shows all projects
		self.dropboxproject = os.path.join(os.environ['USERPROFILE'], 'Dropbox',  self.dropbox_folder) # shows all data after sync

		if not dropbox_folder == "":
			if not os.path.exists(self.dropboxproject):
				os.mkdir(self.dropboxproject)

		# done to ensure consistancy
		self.localproject = self.localproject.replace('\\','/') 
		self.dropboxproject = self.dropboxproject.replace('\\','/')

		self.folders = {'dropbox': self.dropboxproject, 
						'ide': self.localproject}

		if self.dropboxfile == "":
			self.dropboxfile = self.dropboxproject
		if self.localfile == "":
			self.localfile = self.localproject

		self.files = {'dropbox': self.dropboxfile,
						'local': self.localfile}




 	# gui init at beginning
	def gui_init(self):
		self.main_win = Tkinter.Tk()

		self.main_win.iconbitmap("../dropbox-sync-solution-images/dropbox_icon.ico")
		self.main_win.title("BACKUP STUFF!")
		self.main_win.wm_attributes("-topmost", 1)
		self.main_win.resizable(width=0, height=0)
		self.main_win.state(newstate = "normal") # iconic, withdrawn, zoomed
		self.main_win.configure(bg="black")

		self.main_win.update()

		a = [(key, val) for key, val in self.main_win.configure().iteritems()] # dict of .configure


		# self.main_win.withdraw()
		# time.sleep(5)
		# self.main_win.deiconify()

		# self.top = Tkinter.Toplevel()
		# self.top.title("BACKUP STUFF!")
		# self.top.lift(aboveThis = self.main_win)

		#############################################################################
		# cool commenting style!!!													#
		#############################################################################

		self.frame = Tkinter.Frame(bg="black")

		self.set_select_text()


		push_to = Tkinter.PhotoImage(file = "../dropbox-sync-solution-images/push_to_dropbox.gif")
		sync_to = Tkinter.PhotoImage(file = "../dropbox-sync-solution-images/sync_from_dropbox.gif")


		self.push_button = Tkinter.Button(self.frame, image = push_to, 
										command = lambda: self.send_to_dropbox(self.ide_mode))
		self.sync_button = Tkinter.Button(self.frame, image = sync_to, 
										command = lambda: self.retrieve_from_dropbox(self.ide_mode))


		self.push_button.pack()
		self.sync_button.pack()

		self.frame.pack()


		frameselect = Tkinter.Frame(bg="black")
		frameselect2 = Tkinter.Frame(bg="black")
		inputframe = Tkinter.Frame(bg="black")

		frame2select = Tkinter.Frame(bg="black")
		frame2select2 = Tkinter.Frame(bg="black")
		input2frame = Tkinter.Frame(bg="black")

		framelist = [frameselect, frameselect2, inputframe]

		framelist2 = [frame2select, frame2select2, input2frame]


		self.swapframe = Tkinter.Frame(bg = "black")

		self.swap_button = Tkinter.Button(self.swapframe, bg = "lightskyblue1",
											command = lambda: self.swap_gui(framelist, framelist2))
		self.swap_button.pack(fill="x")

		self.swapframe.pack(fill="x")


		self.pack_ide_sol(self.ide_solution_gui(framelist))

		self.local_solution_gui(framelist2)


		self.main_win.mainloop()

	# changes what the selected folders by user are
	def set_select_text(self):

		self.dropbox_select_text = Tkinter.StringVar()
		self.dropbox_select_text.set(self.folders['dropbox'])

		self.idedir_select_text = Tkinter.StringVar()
		self.idedir_select_text.set(self.folders['ide'])

		self.folder_name_text = Tkinter.StringVar()
		self.folder_name_text.set("Project Name ('{currentproject}'):".format(currentproject = self.project_name))

		####

		self.dropbox_file_text = Tkinter.StringVar()
		self.dropbox_file_text.set(self.files['dropbox'])

		self.local_file_text = Tkinter.StringVar()
		self.local_file_text.set(self.files['local'])

		####

		self.select_text_folders = {'dropbox': self.dropbox_select_text, 
									'ide':self.idedir_select_text}

		self.select_text_files = {'dropbox': self.dropbox_file_text,
								'local': self.local_file_text}

	# changes GUI to backup single files instead of folder
	def swap_gui(self, framelist, framelist2):

		self.ide_mode = not self.ide_mode

		#framelist = ORIGINAL IDE/PROJECT MODE
		#framelist2 = SECOND LOCAL FILE MODE

		if self.ide_mode:

			for frameoff in framelist2:
				self.hide_frame(frameoff)
			self.pack_ide_sol(framelist)

		else:

			for frameoff in framelist:
				self.hide_frame(frameoff)
			self.pack_ide_sol(framelist2)

	
	
	# GUI for single file backup
	def local_solution_gui(self, framelist):

		labelframe = framelist[0]
		label2frame = framelist[1]
		inputframe = framelist[2]
 
		self.dropbox_select_button = Tkinter.Button(labelframe, bg = "black", 
													fg = "white", text="Select dropbox file:", 
													command = lambda: self.select_file(self.files['dropbox']),
													relief = 'ridge')


		self.dropbox_select_label = Tkinter.Button(labelframe, wraplength = 250 - self.dropbox_select_button.winfo_reqwidth() - 1,
													 bg = "black", fg = "white", 
													 textvariable = self.dropbox_file_text,
													 justify = "left", font = ("Roboto, 9"),
													 relief = 'flat')

		self.file_select_button = Tkinter.Button(label2frame, bg = "black", 
												fg = "white", text = "Select local file:",
												relief = 'ridge', command = lambda: self.select_file(self.files['local']))

		self.file_select_label = Tkinter.Button(label2frame, wraplength = 250 - self.file_select_button.winfo_reqwidth(),
										bg = "black", fg = "white", 
										textvariable = self.local_file_text,
										justify = "left", font = ("Roboto, 9"),
										relief = "flat", command = lambda: self.open_folder(self.folders['ide']))

		self.dropbox_select_button.pack(side="left")
		self.dropbox_select_label.pack(side="left", fill="x")
		self.file_select_button.pack(side="left")
		self.file_select_label.pack(side="left", fill="x")
	

	# used for changing from file to folder option
	def hide_frame(self, frame):
		frame.pack_forget()


	# initial folder backup option
	def ide_solution_gui(self, framelist):

		frameselect = framelist[0]
		frameselect2 = framelist[1]
		inputframe = framelist[2]

		self.dropbox_select_button = Tkinter.Button(frameselect, bg = "black", relief = "ridge",
													fg = "white", text="Select dropbox folder:", 
													command = lambda: self.browse_dir("Dropbox"))


		self.dropbox_select_label = Tkinter.Button(frameselect, wraplength = 250 - self.dropbox_select_button.winfo_reqwidth() - 1,
													 bg = "black", fg = "white", 
													 textvariable = self.dropbox_select_text,
													 justify = "left", font = ("Roboto, 9"),
													 relief = "flat", command = lambda: self.open_folder(self.folders['dropbox']))

		self.idedir_select_button = Tkinter.Button(frameselect2, bg = "black", relief = "ridge",
													fg = "white", text = "Select local folder:", 
													command = lambda: self.browse_dir('Ide'))

		idedir_label_wrap = self.main_win.winfo_reqwidth() - self.idedir_select_button.winfo_reqwidth()


		self.idedir_select_label = Tkinter.Button(frameselect2, wraplength = 250 - self.idedir_select_button.winfo_reqwidth() - 1, # -1 to not make it bigger than button
												bg = "black", fg = "white", 
												textvariable = self.idedir_select_text,
												justify = "left", font = ("Roboto, 9"),
												relief = "flat", command = lambda: self.open_folder(self.folders['ide']))

		self.project_name_entry = Tkinter.Entry(inputframe)
		self.project_name_label = Tkinter.Label(inputframe, textvariable = self.folder_name_text, 
												bg = "black", fg = "white")


		self.allow_error_window = True

		self.project_name_entry.bind("<Return>", self.update_name)

		self.dropbox_select_button.pack(side="left")
		self.dropbox_select_label.pack(side="left", fill="x")

		self.idedir_select_button.pack(side="left")
		self.idedir_select_label.pack(side="left", fill="x")

		self.project_name_label.pack()
		self.project_name_entry.pack(side="bottom")

		return framelist


	# user error checking
	def allowed_by_windows_folders(self, string):
		not_allowed_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

		allowed = not any(a in string for a in not_allowed_list) # checks if string is allowed to be a windows folder
																 # returns False if string contains illegal character, True otherwise
		return allowed

	def close_window(self, root, event = None):
		self.allow_error_window = True

		try:
			root.destroy()
		except:
			pass


	# CURRENTLY HAS NO USE, USE IN THE FUTURE FOR LONGER IO OPERATIONS
	def start_thread(self, function, event = None):
		t = threading.Thread(target = function)
		t.start()
		t.join()

	def open_folder(self, folder_name):
		folder_name = folder_name.replace("/","\\") # needed since explorer doesn't open / pathnames
		os.system('explorer {}'.format(folder_name))

	# adding on to user error checking
	def filename_must_contain(self, root, error_image, mainroot = None):

		self.allow_error_window = False

		if mainroot	is None:
			mainroot = self.main_win

		mainroot.update()

		# print "x = {} y = {} reqwidth = {} reqheight = {}".format(mainroot.winfo_x(), mainroot.winfo_y(), mainroot.winfo_reqwidth(), mainroot.winfo_reqheight())

		frame = Tkinter.Frame(root)
		frame.pack()

		errorimage_width = 325
		errorimage_height = 50

		erorrimage_width_canvas = int(errorimage_width/2)
		errorimage_height_canvas = int(errorimage_height/2)

		geo_x_off = int(mainroot.winfo_x()-(errorimage_width-mainroot.winfo_reqwidth())/2)
		geo_y_off = mainroot.winfo_y()+mainroot.winfo_reqheight()+errorimage_height/2

		root.overrideredirect(1)
		root.wm_attributes("-topmost", 1)


		root.geometry('325x50+{x_off}+{y_off}'.format(x_off = geo_x_off, y_off = geo_y_off))

		canvas = Tkinter.Canvas(frame, width=errorimage_width, height=errorimage_height)
		canvas.pack()

		canvas.create_image(erorrimage_width_canvas, errorimage_height_canvas, image=error_image) # 325 x 50


		try:
			root.after(4000, lambda: self.close_window(root))
		except:
			pass

		try:
			root.bind("<Button-1>", lambda x: self.close_window(root)) # use lambda x because its a callback
		except:
			pass

		try:
			mainroot.bind("<Configure>", lambda x: self.close_window(root)) # use lambda x because its a callback
		except:
			pass

		try:
			root.bind("<Key>", lambda x: self.close_window(root)) # use lambda x because its a callback
		except:
			pass

		root.mainloop()


	def update_name(self, event = None):


		name = self.project_name_entry.get()

		allowed = self.allowed_by_windows_folders(name)

		if not allowed:

			not_allowed_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

			for a in not_allowed_list:
				name = name.replace(a,"")


		self.project_name = name

		self.folder_name_text.set("Project Name ('{currentproject}'):".format(currentproject = name))


		if self.allow_error_window and not allowed:
			error_image = ImageTk.PhotoImage(file = "../dropbox-sync-solution-images/windows_file_error.png")

			root = Tkinter.Toplevel()

			self.filename_must_contain(root, error_image)


	# helpful for swapping between file/folder layouts
	def pack_ide_sol(self, framelist):

		frameselect = framelist[0]
		frameselect2 = framelist[1]
		inputframe = framelist[2]

		frameselect.pack(fill="x")
		frameselect2.pack(fill="x")
		inputframe.pack()


	def select_file(self, file_name):
		name = file_name # checks if its either dropbox or local file

		newfile = tkFileDialog.askopenfilename(parent=self.main_win,
												title="Select a file:")
		self.files[name.lower()] = newfile



	# allows user to select which folder to set as "project directory"
	def browse_dir(self, folder_name):
		name = folder_name

		newfile = tkFileDialog.askdirectory(parent=self.main_win, 
											title="Select your {} directory:".format(name)) #initialdir = "os.environ['USERPROFILE']" <-- why doesn't this work??
		if not newfile == "":
			self.folders[name.lower()] = newfile 

			self.select_text_folders[name.lower()].set(newfile) # use this after wrapping labels/cutting them off/...label
		# print self.folders['ide'], self.folders['dropbox']

		# self.select_text[name.lower()].set(newfile.split("/")[-1]) # sets string variable from stringvar dictionary as the folder name


	# creates backup of the current folder/file in one directory above the current one
	def create_backup(self, location, original, project):

		# TODO: Create backup for what is being replaced (i.e. create backup for dropbox files if syncing to dropbox)

		path = os.path.join(location, project)
		print original,"--",  path

		if not os.path.exists(path+"BACKUPS"):
			os.mkdir(path+"BACKUPS")

		year = time.localtime()[0]
		month = time.localtime()[1]
		day = time.localtime()[2]
		hour = time.localtime()[3]
		minute = time.localtime()[4]
		second = time.localtime()[5]

		file_name = "%s %s-%s-%s__%s-%s-%s" % (project, year, month, day, hour, minute, second)

		filepath = path+"BACKUPS/"+file_name

		if not os.path.exists(path):
			os.mkdir(path)

		print "original:{} filepath:{}".format(original, filepath)

		shutil.copytree(original, filepath)


	### these commands below use the functions above to sync project, and then either sync to or from the dropbox, depending on the button selected
	
	def sync_project(self, local_directory):
		try:
			shutil.rmtree(os.path.join(self.folders['dropbox'], self.project_name))
		except:
			pass
		print "sending from: {} to: {}".format(local_directory, os.path.join(self.folders['dropbox'], self.project_name))
		shutil.copytree(local_directory, os.path.join(self.folders['dropbox'], self.project_name))


	def retrieve_dropbox(self, local_directory):
		try:
			shutil.rmtree(local_directory)
		except:
			pass
		shutil.copytree(os.path.join(self.folders['dropbox'], self.project_name), local_directory)


	def send_to_dropbox(self, ide_mode):

		if ide_mode and os.path.exists(os.path.join(self.folders['ide'], self.project_name)):
			self.create_backup(self.folders['ide'], os.path.join(self.folders['ide'], self.project_name), self.project_name)

			self.sync_project(os.path.join(self.folders['ide'], self.project_name))
		else:
			pass # TODO: insert code for handling files

	def retrieve_from_dropbox(self, ide_mode):

		if ide_mode and os.path.exists(os.path.join(self.folders['ide'], self.project_name)):
			self.create_backup(self.folders['dropbox'], os.path.join(self.folders['dropbox'], self.project_name), self.project_name)

			self.retrieve_dropbox(os.path.join(self.folders['ide'], self.project_name))	
		else:
			pass


## REPLACE THESE VALUES WITH YOUR PREFERRED LOCATIONS IF NECESSARY
ide_name = ""
project_name = ""
workspace_name = ""
fileselect = ""
dropboxfile = ""
dropbox_folder = "Sync Solution"

if __name__ == "__main__":
	dropbox = DropBox_SYNC(ide_name = ide_name, project_name = project_name, dropbox_folder = dropbox_folder, 
						fileselect = fileselect, dropboxfile = dropboxfile, workspace_name = workspace_name)
	dropbox.gui_init()
