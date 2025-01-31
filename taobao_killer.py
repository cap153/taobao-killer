from DrissionPage import Chromium
import datetime

# 创建对象
page = Chromium(9223).latest_tab

# 指定秒杀时间，格式为“时:分:秒.毫秒”，无需设定日期
kill_time = "19:00:00.00000000"

# 打开淘宝网页
page.get("https://cart.taobao.com/")
# 等待登录完成，直到购物车全选按钮出现，超时时间我设置为1分钟
page.ele('全选',timeout=60,index=-1).click()

while(True):
    # 获取当前时间
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    print(now) # 打印当前时间测试
    # 判断当前时间是否到达了秒杀时间
    if(now>kill_time):
        try:
            # 按需解开注释，二次判断商品是否全选(根据全选框class是否变成ant-checkbox ant-checkbox-checked来判断是否成功全选)
            # while page.ele('.ant-checkbox',timeout=0.1):
                # 没有全选的情况，点击购物车全选按钮
                # page.ele('全选',index=-1).click()
            # 点击结算按钮
            page.ele('结算',index=-1).click()
            # 下单商品
            page.ele('提交订单',timeout=60).click()
            # 自动填充密码(需要修改成你自己的支付密码)
            # page.ele('x://*[@id="payPassword_rsainput"]').input("123456")
            # 确定
            # page.ele('x://*[@id="validateButton"]').click()
            break
        except Exception as err:
            # 如果发生任何异常都进行捕捉，防止浏览器退出
            print("%s\n发生了错误，请手动完成后续步骤"%err+input())
    # 判断当前秒数是不是0，实现间隔一分钟刷新页面，防止掉登录
    if(datetime.datetime.now().second == 0):
        while(True):
            page.refresh() # DrissionPage的页面刷新方法，内置了wait.load_start()程序会自动等待加载结束
            try:
                # 等待全选按钮加载
                page.wait.ele_displayed('全选')
                break # 按钮加载成功说明没有问题，跳出循环
            except:
                # 没有成功加载按钮说明出现了错误，无论什么错误都继续循环再次刷新页面
                continue
        # 再次全选购物车
        page.ele('全选',index=-1).click()

# 成功的信息输出和测试时的程序暂停
input('恭喜，抢购成功')
