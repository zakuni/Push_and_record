# -*- coding: utf-8 -*-
require 'rubygems'
require 'appscript'
require 'socket'
require 'thread'
require "ffmpeg"
include FFMpeg
include Appscript

i = 0

QP = app('QuickTime Player')

def rec_start
  QP.activate
  QP.new_audio_recording
  QP.documents[1].start()
end

def rec_stop
  QP.documents[1].stop()
  QP.documents[1].close()
end

def convert_and_delete(file, i)
  if i == 0
    a = "a"
    puts a
  elsif i == 1
    a = "b"
    puts a
  end
  time = Time.now
  sec = Time.now.sec
  puts "time.now = #{time.sec}"
  puts "sec = #{sec}"
  convert "~/Movies/#{file}", :to => "~/Movies/#{a}.mp3" do end.run  #movをmp3に変換
  puts "sec_after = #{sec}"
#  `rm ~/Movies/オーディオ収録.mov` #オーディオ収録.movは削除する
end

sensors = Array.new(4, 980) # センサーの番号と値を入れる配列

rec = 0


t = Thread.new do
  loop do
    sock = TCPSocket.open("127.0.0.1", 20000) # 127.0.0.1(localhost)の20000番へ接続

    ik = sock.read()
    sensor_and_value = ik.slice(/Sensor.*/)
    sensor = sensor_and_value.slice(/\d+/) # センサー番号
    value = /\d*:\s/.match(sensor_and_value).post_match # センサーの値

    sensors[sensor.to_i] = value.to_i
    
    puts "sensor0 #{sensors[0]}"

    if (sensors[0] < 950) #ドアが開いたら録音開始
      unless rec == 1
        rec = 1
        puts rec
        rec_start
      end
    else            # ドアが閉まったら録音終了してmp3にコンバート
      unless rec == 0
        rec = 0
        puts rec
        rec_stop
        renamed = "#{Time.now.min}-#{Time.now.sec}"
        File.rename(File.expand_path("~/Movies/オーディオ収録.mov"), File.expand_path("~/Movies/#{renamed}.mov"))
        convert_path = (File.expand_path("~/Movies/#{renamed}"))
        `ffmpeg -i "#{convert_path}.mov" "#{convert_path}.mp3"`
        File.delete(File.expand_path("~/Movies/#{renamed}.mov")) # movファイルは消す
      end
    end
    sleep(0.1)
  end
sock.close # ソケットを閉じる
end

t.join
