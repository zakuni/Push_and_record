require 'rubygems'
require 'appscript'
include Appscript

QP = app('QuickTime Player')
QP.activate
QP.new_audio_recording
QP.documents[1].start()
sleep 2
QP.documents[1].stop()

