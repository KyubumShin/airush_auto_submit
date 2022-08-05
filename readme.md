# CLOVA AIRUSH Auto Submit

## requirement
```
fastapi[all]
```

## 사용 전 세팅
* nsml login 필요
* nsml_id, data_name 채우기
```
nsml_id = ""  # 사용중인 nsml 아이디
data_name = "" # 참여중인 대회 데이터셋
```

## 사용법
1. submit.csv에 제출할 Session, model을 작성 (string 타입도 OK)

![image](https://user-images.githubusercontent.com/69576436/180590081-a56c079e-a870-49e1-95c8-3cc941214a03.png)

2. submit.py를 실행
  * -wt [대기 하고 싶은 시간] : 첫 제출까지 대기할 시간 설정 가능

```
python submit.py -wt [첫 제출까지의 대기시간 Default : 0]
```
3. submit.db가 생성되고 이곳에 Session, model, Score가 저장

![image](https://user-images.githubusercontent.com/69576436/180590037-bec280aa-0ee3-43c2-a3bc-116f2c8bf694.png)

## 메모 및 정리용 툴 업데이트
Fastapi를 이용해서 그동안 submit.db에 저장된 내용들을 볼 수 있게 만들어 보았습니다. (LB스코어로 Sorting해서 보여줍니다)
* 단 Add Seesion Memo를 통해서 메모를 생성하지 않으면 내역에서 보이지 않습니다
![캡처](https://user-images.githubusercontent.com/69576436/183079870-cbefd769-df44-409e-aa6d-cb780d7c5c1d.PNG)

Add Session Memo를 통해서 nsml에 메모를 추가함과 동시에 DB에 저장하여 
nsml memo에 다음과 같이 저장됩니다
> model : {모델 내용} , Desc: {Description 내용}

submit.py로 제출한 내용은 Session 번호를 누르면 다음과 같이 볼 수 있습니다.
![4](https://user-images.githubusercontent.com/69576436/183080608-d5fbe90f-8754-4fc5-82b2-c58e7e5cc020.PNG)

## 앞으로 업데이트 예정 내역
* Fastapi BackgroundTask를 이용한 Auto Submit 기능
* Sorting 기능
