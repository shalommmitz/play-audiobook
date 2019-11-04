<p align="center">
  <h3 align="center">Play Audiobook</h3>

  <p align="center">
    Very simple to operate player of audio books
  </p>
</p>
<br>
Some persons, especially elderly persons that are visually challenged, need as simple as possible user interface.
For those persons, this project was created.
It is assumed that another person puts the mp3 (or other VLC-playable format) audio files under the "book" folder.
To play the book, you need to touch the screen.
To pause playing, you need to touch the screen.
This is it. The whole user interface.


## Prerequisites and Environment
This project was written and tested using Ubuntu 18.04 and Python 2.7
You will need VLC and:

    sudo apt-get install python-dbus

## The Audio Book

For simplicity, only one audiobook is played at any time. The audio files of this book are put in the folder "./book".
If this software detects that the actual audiobook was replaced, it will start playing the first file. Otherwise, it will start to play the audio file last heard.

## Author

**Shalom Mitz** - [shalommmitz](https://github.com/shalommmitz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE ) file for details.

