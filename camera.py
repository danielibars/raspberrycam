import psutil
import os, signal
import gphoto2 as gp


class Camera:
    def kill_ptp_camera_process(self):
        for proc in psutil.process_iter(["pid", "name"]):
            # check whether the process name matches
            if proc.info["name"] == "PTPCamera":
                proc.kill()

    def __init__(self):
        self.kill_ptp_camera_process()
        self.context = gp.Context()
        self.camera = gp.Camera()
        self.camera.init(self.context)

    def disconnect_camera(self):
        self.camera.exit()

    def killgphotoprocess():
        processes = psutil.process_iter()
        for process in processes:
            if "gphoto2" in process.name():
                print(f"Killing Process ID: {process.pid}, Name: {process.name()}")
                os.kill(process.pid, signal.SIGKILL)

    def is_awake(self):
        try:
            self.camera.get_summary(self.context)
            return True
        except gp.GPhoto2Error:
            return False

    def trigger_capture(self):
        print("Capturing image")
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        print("Camera file path: {0}/{1}".format(file_path.folder, file_path.name))
        target = os.path.join("/home/pi/Documents/", file_path.name)
        print("Copying image to", target)
        camera_file = self.camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(target)

    # def autodetect(self):
    #     autodetects = self.camera.autodetect()
    #     for autodetect in autodetects:
    #         camera_name, usb_port = autodetect
    #         print(camera_name)

    # def delete_all_files(camera, path='/'):
    #     # Get list of files
    #     files = camera.folder_list_files(path)
    #     for file, _ in files:
    #         camera.file_delete(path, file)
    #         print(f'Deleted file: {path}{file}')

    #     # Get list of folders
    #     folders = camera.folder_list_folders(path)
    #     for folder, _ in folders:
    #         # Recursively delete files in subfolders
    #         delete_all_files(camera, path + folder + '/')

    # def download_files(camera, path='/', target_folder='/home/pi/Documents/photoapi/pics/'):
    #     # Get list of files
    #     files = camera.folder_list_files(path)
    #     for file, _ in files:
    #         # Check if file is JPEG or CR2
    #         if file.endswith('.JPG') or file.endswith('.CR2'):
    #             # Get the file
    #             camera_file = camera.file_get(path, file, gp.GP_FILE_TYPE_NORMAL)
    #             # Save the file
    #             target_path = os.path.join(target_folder, file)
    #             camera_file.save(target_path)
    #             print(f'Downloaded file: {target_path}')

    #     # Get list of folders
    #     folders = camera.folder_list_folders(path)
    #     for folder, _ in folders:
    #         # Recursively download files in subfolders
    #         download_files(camera, path + folder + '/', target_folder)

    # def list_folders(camera, path="/"):
    #     folders = camera.folder_list_folders(path)
    #     for folder, _ in folders:
    #         print(f'Folder: {path}{folder}')
    #         # Recursively list subfolders
    #         list_folders(camera, path + folder + '/')

    # def get_battery_level(camera):
    #     # Get configuration
    #     config = camera.get_config()

    #     # Find the battery level configuration
    #     ok, battery_level = gp.gp_widget_get_child_by_name(config, 'batterylevel')
    #     if ok >= gp.GP_OK:
    #         # Get the battery level value
    #         battery_level_value = gp.check_result(gp.gp_widget_get_value(battery_level))
    #         return battery_level_value
    #     else:
    #         return None
