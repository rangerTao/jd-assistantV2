#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jd_assistant import Assistant
import random
import datetime
import sys, getopt
import optparse

if __name__ == '__main__':
    """
    重要提示：此处为示例代码之一，请移步下面的链接查看使用教程👇
    https://github.com/tychxn/jd-assistant/wiki/1.-%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B%E7%94%A8%E6%B3%95
    """
    #area = '19_1607_4773'  # 区域id
    args_sdk = ''
    args_num = 0
    asst = Assistant()  # 初始化
    asst.login_by_QRcode()  # 扫码登陆
    #asst.get_single_item_stock(100006394713,1,'19_1607_4773')
    # 获取参数信息
    usage = "mainV2.py -s <args_sdk> -n <args_num>"
    parser = optparse.OptionParser(usage)
    parser.add_option('-s','--sku',dest='sku',type='string',help='sku id',default=0)
    parser.add_option('-n','--num',dest='num',type='int',help='sku num',default=1)
    options,args = parser.parse_args()
    print('options :',options)

    args_sdk= options.sku
    args_num = options.num
    print ("输入的SKU_ID：%s",args_sdk)
    print ("输入的SKU_num：%s",args_num)

    model_type = input("请输入购买类型(1.定时预约抢购 2.正常有货购买 3.正常定时购买)：")
    if model_type == '1':
        print("定时预约抢购...")
        if args_sdk == '' :
            sku_id = input("请输入一个sku_id:")
            # sku_id = '100012043978'
            asst.print_item_info(sku_id)
        else:
            sku_id = args_sdk
        
        if args_num == 0:
            input_num = input("请输入抢购数量:")
            asst.print_item_info(input_num)
        else:
            input_num = args_num

        reserve_info = asst.get_reserve_info(sku_id)
        reserve_time = reserve_info.get("yueStime")
        buy_time = reserve_info.get("qiangStime")
        print("预约时间:",reserve_time)
        print("抢购时间:",buy_time)
        # 开始预约
        if reserve_time :
            asst.make_reserve(sku_id, reserve_time + '.000')
        else:
            print('获取预约时间失败')
        # 开始抢购
        if buy_time :
            rand_msecond = random.randint(1,9) * 1000
            buy_time = buy_time + '.000'
            #buy_time = buy_time + "." + str(rand_msecond)
        else:
            print('获取抢购时间失败')
            buy_time = input("请输入抢购时间(2020-03-04 00:59:59.000):")
        #asst.exec_reserve_seckill_by_time(sku_id=sku_id,buy_time=time, retry=10, interval=1,num=1)
        asst.exec_seckill_by_time(sku_ids=sku_id,buy_time=buy_time, retry=15, interval=0.2,num=input_num)
    elif model_type == '2':
        print("正常有货购买...")
        sku_ids = input("请输入一个或多个sku_id:")
        area = input("请输入area_id:")
        asst.buy_item_in_stock(sku_ids=sku_ids, area=area, wait_all=False, stock_interval=5)

    elif model_type == '3':
        print("正常定时购买...")
        sku_ids = input("请输入一个或多个sku_id:")
        buy_time = input("请输入定时购买时间(2020-03-04 00:59:59.000):")
        asst.clear_cart()       # 清空购物车（可选）
        asst.add_item_to_cart(sku_ids=sku_ids)  # 根据商品id添加购物车（可选）
        asst.submit_order_by_time(buy_time=buy_time, retry=10, interval=5)  # 定时提交订单
