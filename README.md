# 碎碎念，正文跟操作方式請跳過這段
請容許我碎碎唸一小段話
這是我第一個開源的軟體，其實也只有一個初步架構，正在慢慢努力寫，啊哈哈~
在出社會前是沒有接觸過任何軟體跟相關知識....，感覺會廢話太多，不說了

目前只有寫一個雛雛雛雛雛雛型。
這個軟體的誕生，其實是因為我莫名地到傳統產業當行政
然後有許多零碎的事情、重複的事情、需要每天做，甚至是公司的庫存都是手寫在本子上，也沒有資料庫
補充一個:其實我是想找軟體工程師的工作，但是無奈沒有甚麼學歷、作品，有的只有滿滿的興趣跟熱情
所以每天在做行政工作時，心裡想著的都是我好想寫code，好想把我的想法實現出來；所以就寫了這隻程式
然後開始我是寫只用在我上班公司的code，但後來想一想，也可能有其他傳統產業或是其他產業，也需要這些類似功能
所以就打掉重寫，慢慢把它改成，可以供所有人使用的辦公室軟體?感覺說商用程式怪怪的，商用感覺是要花錢買，但這不是。

這個軟體主要就是用pyqt6寫的一個GUI介面，供辦公室使用有各種功能跟庫存資料庫的軟體

我的想法是，有一個主要運行的主程式，然後把各個功能都分包到其他py檔案，這樣在擴充或是優化都會比較方便。
現在架構是，運行時候，需要先去設定資料庫，我使用的是mysql，所以要先現下載mysql
在剛運行程式時，如果沒有設定資料庫的帳號密碼，就需要先設定，不然他就無法繼續執行。
這邊說得無法執行不是無法打開軟體，而是執行時候的登入畫面，如果沒有設定就按註冊帳號或是登入，他是無法執行的
需要先在軟體下面點設定資料庫，把資料庫設定好，才可以繼續執行
因為我的註冊帳號密碼...，等等都是要把存在資料庫中的登入帳號資料表。
我的想法是有一個處理註冊帳密的表，然後登入成功後，會在創建這個帳號的資料庫，此時就換轉換資料庫為這個帳號的。
那我就可以在這個帳號的資料庫中做各種處理，像是個人資料....或是這個帳號使用者的各種商品庫存的資料庫...等等
甚至是我可以在個人資料那邊寫一個使用功能的設定，他就可以改變我的軟體登入後的各個功能選擇。
因為每間不同公司需要的功能都不同，如果各種功能一直擴充，到時候，只是讓使用者混亂，在個人資料設定裡面可以選擇會使用得功能，
那我再登入成功後，就可以創建出有選擇的功能在把它放到登入畫面上。
當然這都是我的雛型想法，可能會遇到各種問題。

然後一開始設定資料庫我儲存資料庫帳號密碼的方式是用config.ini檔案，把資料儲存在這裡，這樣我再登入mysql才有帳號密碼跟端可以選擇。

有一些py檔案目前沒有作用，因為是一開始只針對我的公司寫的，但要開源讓大家使用，顯然不能這樣處理；所以就還丟在那邊沒處理。


啊哈排版好尷尬，但先這樣，我也不會用，等之後摸索好在來整理排版
以上都是碎碎念廢話，懶得刪除了(以後有緣再來處理)

# 稍微介紹跟使用方式教學
### 目前有的功能:
<p>1. 庫存功能:我的目的主要是處理工廠的庫存，因為每天都要點貨、出貨、退貨...等等，有這個資料庫，就可以管理我的各商品存貨。</p>
<p>2. 商品資料庫功能:建立商品資料庫，才可以設定庫存量，有這個商品資料庫，在後續可以關聯庫存、出貨、進貨原料、製作需求...等等。
</p>

### 使用方式:
<p>1. 這畢竟是資料庫程式，得先下載資料庫，我所使用的是開源的資料庫Mysql，所以在使用前請先安裝好Mysql。<br><br>
這邊是<a href="https://www.mysql.com/" target="blank">MySQL</a>官方，沒有下載的話請點選連結<br>並照著下面步驟下載並安裝<a href="#mysql下載跟安裝教學">MySQL下載跟安裝教學</a>。
</p>
<p>2. 下載主程式，上面是開源的code，如果看得懂的，可以自己載回去改，不然就是等我慢慢更新程式了<br>主程式在上面的dist/main.exe</p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>

# MySQL下載跟安裝教學
到官方網站下載MySQL，下面會放流程圖片，不知道怎麼安裝的請照步驟下載，目前只有windows系統，其他的可能要自己研究囉。
  
[MySQL](https://www.mysql.com/) 官方網站。

## 步驟說明

1. 到官方網站下載MySQL安裝檔。以下是詳細操作步驟，點DOWNLOADS：
   ![步驟1](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_1.jpg)
   
2. 點MySQL Community (GPL) Downloads »：
   
   ![步驟2](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_2.jpg)
   

3. 點MySQL Installer for Windows：
   
   ![步驟3](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_3.jpg)
   

4. 我是選版本比較新的，然後點下面檔案比較大的那個: ![步驟4](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_4.jpg)
   
   

5. 他會問要不要登入或註冊，如果沒需求就點下面直接下載: ![步驟5](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_5.jpg)
   

6. 下載好後，就開始安裝吧: ![步驟6](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_6.jpg)
   

7. 雖然我不是所有功能都使用，但就點全部下載吧: ![步驟7](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_7.jpg)
   

8. 這些是各種的功能，沒問題就點吧!: ![步驟8](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_8.jpg)
   

9. 這邊會是先下載這些功能: ![步驟9](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_9.jpg)
   

10. 下載後就是安裝: ![步驟10](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_10.jpg)
    

11. 安裝後繼續下一步: ![步驟11](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_11.jpg)
    

12. 這邊要來安裝Server跟Router: ![步驟12](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_12.jpg)
    

13. 沒意外就照上面的繼續執行下一步驟: ![步驟13](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_13.jpg)
    

14. 第十四步驟: ![步驟14](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_14.jpg)
    
    第十四步驟文字

15. 第十五步驟: ![步驟15](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_15.jpg)
    
    第十五步驟文字

16. 第十六步驟: ![步驟16](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_16.jpg)
    
    第十六步驟文字

17. 第十七步驟: ![步驟17](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_17.jpg)
    
    第十七步驟文字

18. 第十八步驟: ![步驟18](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_18.jpg)
    
    第十八步驟文字

19. 第十九步驟: ![步驟19](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_19.jpg)
    
    第十九步驟文字

20. 第二十步驟: ![步驟20](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_20.jpg)
    
    第二十步驟文字

21. 第二十一步驟: ![步驟21](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_21.jpg)
    
    第二十一步驟文字

22. 第二十二步驟: ![步驟22](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_22.jpg)
    
    第二十二步驟文字

23. 第二十三步驟: ![步驟23](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_23.jpg)
    
    第二十三步驟文字

24. 第二十四步驟: ![步驟24](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_24.jpg)
    
    第二十四步驟文字

25. 第二十五步驟: ![步驟25](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_25.jpg)
    
    第二十五步驟文字

26. 第二十六步驟: ![步驟26](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_26.jpg)
    
    第二十六步驟文字

27. 第二十七步驟: ![步驟27](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_27.jpg)
    
    第二十七步驟文字

28. 第二十八步驟: ![步驟28](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_28.jpg)
    
    第二十八步驟文字

29. 第二十九步驟: ![步驟29](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_29.jpg)
    
    第二十九步驟文字

30. 第三十步驟: ![步驟30](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_30.jpg)
    
    第三十步驟文字

31. 第三十一步驟: ![步驟31](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_31.jpg)
    
    第三十一步驟文字

32. 第三十二步驟: ![步驟32](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_32.jpg)
    
    第三十二步驟文字

33. 第三十三步驟: ![步驟33](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_33.jpg)
    
    第三十三步驟文字

34. 第三十四步驟: ![步驟34](https://github.com/williamkai/Pyqt6_office_project/blob/main/github_readme_jpg/mysql_34.jpg)
    
    第三十四步驟文字

## 注意事項

- 確保你的系統符合MySQL的安裝要求。
- 如果遇到任何問題，可以參考[官方文檔](https://dev.mysql.com/doc/)或在論壇上尋求幫助。
