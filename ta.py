1、在github上创建项目

2、使用git clone https://github.com/xxxxxxx/xxxxx.git克隆到本地

3、编辑项目

4、git add . （将改动添加到暂存区）

5、git commit -m "提交说明"

6、git push origin master 将本地更改推送到远程master分支。

这样你就完成了向远程仓库的推送。

如果在github的remote上已经有了文件，会出现错误。此时应当先pull一下，即：

git pull origin master

然后再进行：

git push origin master


# 查看分支名
git rev-parse --abbrev-ref HEAD

第三次测试合并
