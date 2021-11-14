# THU Net Authentication

终端一键登录清华大学校园网 Python 脚本。

## 环境配置

Clone 本项目：

```
git clone https://github.com/liang2kl/thu-net-auth.git
cd thu-net-auth
```

安装依赖：

```shell
# macOS
pip3 install -r requirements.txt
# Windows
pip install -r requirements.txt
```

## 使用

```shell
# macOS
python3 auth.py [--logout] [--persistent] [--clear]
# Windows
python auth.py [--logout] [--persistent] [--clear]
```

- `--persistent` 或 `-p`：在第一次登陆输入用户名和密码后，将其储存到系统 Keychain 中，后续无需再次输入，建议使用
- `--clear` 或 `-c`：清除 Keychain 中保存的用户名和密码
- `--logout` 或 `-o`：下线，若无此项参数则为登陆
