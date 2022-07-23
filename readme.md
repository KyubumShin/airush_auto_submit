# CLOVA AIRUSH Auto Submit

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

