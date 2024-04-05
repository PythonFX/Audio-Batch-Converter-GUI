import os, sys, subprocess
from enum import Enum
from tkinter import Tk, Listbox, END, Checkbutton, IntVar, Radiobutton, StringVar, Frame, Label
from tkinterdnd2 import DND_FILES, TkinterDnD


class AudioType(Enum):
    WAV = 'wav'
    FLAC = 'flac'
    MP3 = 'mp3'
    M4A = 'm4a'
    OGG = 'ogg'


def get_convert_command(audio_type):
    if audio_type == AudioType.WAV:
        return 'pcm_s16le'
    if audio_type == AudioType.FLAC:
        return 'flac'
    if audio_type == AudioType.MP3:
        return 'libmp3lame'
    if audio_type == AudioType.M4A:
        return 'aac'
    if audio_type == AudioType.OGG:
        return 'libvorbis'


def get_bitrate_command(audio_type):
    if audio_type == AudioType.MP3:
        return '-q:a 0'
    if audio_type == AudioType.M4A:
        return '-b:a 400k'
    if audio_type == AudioType.OGG:
        return '-b:a 320k'
    return ''


def convert_audio(audio_file_path, delete_original):
    # Parse the file path to separate the directory and filename
    dir_name = os.path.dirname(audio_file_path)
    base_name = os.path.basename(audio_file_path)
    file_name, file_ext = os.path.splitext(base_name)
    counter = 1

    # Define the output WAV file path
    output_file_path = os.path.join(dir_name, f'{file_name}.{target_audio_type.value}')
    while os.path.exists(output_file_path):
        output_file_path = os.path.join(dir_name, f'{file_name}_{counter}.{target_audio_type.value}')
        counter += 1
    convert_command = get_convert_command(target_audio_type)
    bitrate_command = get_bitrate_command(target_audio_type)

    command = ['ffmpeg', '-i', audio_file_path, '-vn', '-acodec', convert_command, '-ar', '44100', '-ac', '2']
    command += bitrate_command.split()
    command.append(output_file_path)

    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW
    else:
        creation_flags = 0  # No flag needed for non-Windows platforms

    try:
        print(command)
        result = subprocess.run(command, check=True, creationflags=creation_flags)
        print(result)
        print(f"Conversion successful: {audio_file_path} to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

    # Check if the user wants to delete the original audio file
    if delete_original:
        os.remove(audio_file_path)
        print(f"Deleted original file: {audio_file_path}")

    return output_file_path


def on_drop(event):
    # event.data contains the paths to the dropped files
    files = root.tk.splitlist(event.data)
    delete_original = delete_var.get()  # Check the state of the checkbox
    for f in files:
        if not f.lower().endswith(('.wav', '.flac', '.ape', '.m4a', '.aac', '.mp3', '.ogg')):
            print(f"Skipping unsupported file: {f}")
            continue
        try:
            output_file_path = convert_audio(f, delete_original)
            listbox.insert(END, output_file_path)
            print(f"Converted {f} to {output_file_path}")
        except Exception as e:
            print(f"Error converting {f}: {e}")


if __name__ == "__main__":
    # Create the main window
    root = TkinterDnD.Tk()
    root.title('音频批量转换')
    root.geometry('600x500')
    target_audio_type = AudioType.WAV

    # Frame for the conversion list
    conversion_frame = Frame(root)
    conversion_frame.pack(fill="both", expand=True, side="left")

    # Create a listbox to display converted files
    listbox = Listbox(conversion_frame)
    listbox.pack(fill="both", expand=True)

    # Checkbox to decide whether to delete the original files
    delete_var = IntVar(value=0)  # Default is not to delete
    delete_checkbox = Checkbutton(conversion_frame, text="转换后删除源文件", variable=delete_var)
    delete_checkbox.pack()

    # Frame for the audio format selection
    format_frame = Frame(root)

    format_frame.pack(fill="both", expand=True, side="right")

    # Label for the audio format selection
    format_label = Label(format_frame, text="选择目标音频格式：")
    format_label.pack(anchor='w')

    # Variable to store the selected audio format
    selected_audio_type = StringVar(value=AudioType.WAV.value)  # Default selection

    # Function to update the selected audio type
    def update_selected_audio_type():
        global target_audio_type
        target_audio_type = AudioType(selected_audio_type.get())

    # Radio buttons for selecting the target audio format
    for audio_type in AudioType:
        Radiobutton(format_frame, text=audio_type.value.upper(), variable=selected_audio_type,
                    value=audio_type.value, command=update_selected_audio_type).pack(anchor="w")

    # Enable drag-and-drop on the listbox
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    # Start the Tkinter event loop
    root.mainloop()
