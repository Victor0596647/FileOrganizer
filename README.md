# File Organizer

I made this python scipt because I download alot things on my pc and it gets messy. So then I wanted to organize my files automatically and with a different and customizable way of doing it unlike most programs I found online.

# How to use
To be able to use it the program, you need to edit the `filterConfig.json` in order to filter files to your liking.
<h2>JSON Configuration</h2>
Your json file should start out like this:

```json
{
	"locations": [
		{
			"path": "",
			"fileExcepts": [
				""
			],
			"folderFilter": [
				{
					"name": "",
					"exts": [
						""
					]
				}
			]
		}
	]
}
```

`"locations"` - Is an array where it can store multiple objects that each contain the path to the desired location to be organized and their own filter parameters.

`"path"` - contains a string path location to the desired location.

`"fileExcepts"` - contains an array of strings that take in file extensions or filenames or file specifiers and excludes them from being organized.

`"folderFilter"` - similar to the `"locations"` variable, this contains an array of folder objects that contain the name of the folder and extentions to sort the matching files into.

`"name"` - basically just contains the name of the folder/directory

`"exts"` - similar to `"fileExcepts"`, this contains an array of strings that also contains file extensions, filenames, or file specifier for the current folder/directory.

Here's an example of how the config could look like:

```json
{
	"locations": [
		{
			"path": "C:\\Users\\[username]\\Downloads",
			"fileExcepts": [
				"ini"
			],
			"folderFilter": [
				{
					"name": "Zips",
					"exts": [
						"zip",
						"rar",
						"7z",
						"gz"
					]
				},
				{
					"name": "Media",
					"exts": [
						"jpg",
						"jpeg",
						"png",
						"bmp",
						"mp4",
						"mp3",
						"wav",
						"gif",
						"mov",
						"mkv",
						"m4a"
					]
				},
				{
					"name": "Installers",
					"exts": [
						"exe",
						"msi"
					]
				},
				{
					"name": "Document Files",
					"exts": [
						"pdf",
						"ppt",
						"txt",
						"csv"
					]
				},
				{
					"name": "Misc",
					"exts": [
						"*"
					]
				}
			]
		}
	]
}
```

<b>Note</b>: You can also have multiple different locations for the file to sort at once.

<h3><b>File Specifying</b></h3>

Now let's get into the advanced features, the strings that are within `"exts"` or `"fileExcepts"` aren't only limited to file extensions and file names, they also can contain certain characters that can make it more selective.

These characters are `*` and ` `` `.

<b>`*`</b> - the asteriks character can be used to specify any file if used like this `"*"`. 
* It can specify any file with the matching extension like this `"*.txt"` (similar to `"txt"`).
* And it specify any file with the matching filename like this `"filename.*"`

<br>

<b>` `` `</b> - the two backtick characters function as a keyword search and there needs to be two of them in order to work, kind of like the quotation marks.
* Using them like this ``` "`f`.txt" ``` will specify files that have the keyword 'f' in the filename and match file extension.
* Using them like this ``` "filename.`x`" ``` will specify files that have the keyword 'x' in their file extension and if they also match the filename
* And finally they can be used like this ``` "`f`.`x`" ``` which is pretty self-explanatory.

The asteriks and backticks can also be combined to form something like this ``` `f`.* ``` or ``` *.`x` ```.

<br>
Here's another example making use of the <b>file specifiers</b>:

```json
{
	"path": "C:\\Users\\[username]\\Saved Pictures",
	"fileExcepts": [
		""
	],
	"folderFilter": [
		{
			"name": "Wallpapers",
			"exts": [
				"`wallpaper`.*" 
			]
		},
		{
			"name": "Art Stuff",
			"exts": [
				"`sketch`.*",
				"`art`.*"
			]
		},
		{
			"name": "Krita projects",
			"exts": [
				"*.kra"
			]
		},
		{
			"name": "Misc Pictures",
			"exts": [
				"*"
			]
		}
	]
}
```

<h2>Running the program</h2>

Running the program is simple, just make sure you python installed and run it in your terminal by using `py fileOrganizer.py` and it should work. Oh and make sure you put the python file somewhere where it isn't in one of the sorting locations or it might also sort the main file itself. 

**Note:** You are required to install the **[Rich module](https://github.com/Victor0596647/FileOrganizer/commit/a891f8599e636274448bc0f536ca78c6d7f8733e)** as of now.