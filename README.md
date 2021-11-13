# Science project


# How to run program
<ul style="list-style-type: square">
    <li><h2>Run teacher program from teacher's PC </h2> </li>

    python /teacher/main.py

<p>then it starts web server.</p>
    <li><h2>Run raspberrypi student monitor agent </h2></li>

> You need to know *teather system's ip address* and *raspberrypi device's ip address*.

>Run ssh to connect to raspberrypi with terminal

```
ssh pi@192.168.1.180
```
>Then, run student monitor like below.</p>

```
cd ~\work\sciproject\raspberrypi
python3 student.py kevin 192.168.1.176
```

<li>
  <h2>측정값</h2>
  <ul style="list-style-type: upper-roman">
    <li>
    학생의 화면방향(x), 화면과 직각방향(y)의 몸의 기울임 상태
    </li>
    <li>
    측정용 카메라에 인식된 얼굴의 위치와 크기
    </li>
    <li>
    측정용 카메라에 얼굴이 인식되는 빈도, (예) 최근 몇초간 화면에 잡히지 않음 등/ 최근 몇초간 화면에서 얼굴이 중앙으로부터 XX% 벗어남
    </li>  
    <li>
    gyro 센서에서 자세가 특정 영역에서 유지되는 시간 (예) 최근 몇초간 좋지 않은 각도를 유지함/
    </li>   
  </ul>
</li>
</ul>


# 사진 및 그래프 자료

촬영 예정

## 의자에 앉은 기울기 자세 측정
의자에 앉은 기울기 자세와 각도 측정 라인, 화면에 표시된 기울기 값을 그래프로

## 화면에서 얼굴 detection 
화면에서 인식된 얼굴 위치와 모니터 화면에 표시되는 값 표현

## 시간의 진행에 따른 측정 그래프
수업중 기울기 변화량 측정 수업중 센서 착용및 값저장
수업중 화면 캡쳐와 위치 변화 그래프

## 

# Software 개발 상세 설명


# OS (Operating System)
Windows - Microsoft

Unix

Linux, Android
|
Mac, IOS
 <br/>
 ls
 cmd
 pwd
 mkdir
 rmdir
 source
 rm
 mv

 <br/>

 ## UI
 user interface
 ## GUI
 Graphical User Interface

 Lius Kobals <<---
 Linux 
  : upgradig... 

## Linux
where to use???
PC => 
Personal usage, game, etc.
Office usage,
Linux <<===== >>
  Ubuntu, RedHat, ...etc.


## Hardware
CPU >>> Intel, AMD, ARM