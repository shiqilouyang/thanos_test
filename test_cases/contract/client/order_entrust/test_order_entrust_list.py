#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
from common.mongodb_operate import MongoDb
from config.contract_enum import orderTypes, orderSides, positionSides, timeInForces, orderStates
from model.symbol import symbol as s
from operation.contract.client.order_entrust.order_entrust_list import order_entrust_list
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_order_entrust_list():
    '''
      查看全部委托:
            1, 返回结果随机取出一个值与数据库对比
            2, 分页:
               page,size = (1, 2) 的最后一个值与 page,size = (2, 1)的第一个值相等
            3, 时间搜索:
                 1),接口返回值随机选择一个 createdTime,最为createdTime或者 endTime 传参
                 2),返回值的endTime应该小于随机选择的createdTime 或者 随机选择的createdTime应该小于返回值的createdTime
            4, endTime 与 startTime 都传的情况下，不是取两者之间的值
                     (createdTime > startTime) or (createdTime < endTime)

    '''
    @pytest.mark.single
    @pytest.mark.parametrize("scene,endTime,forceClose,page,size,startTime,state,symbol,type,code,except_msg",
                             api_order_entrust["order_entrust_list"])
    def test_order_entrust_list(self,scene,endTime,forceClose,page,size,startTime,state,symbol,type,code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{endTime}-{forceClose}-{page}-{size}\
                    -{startTime}-{state}-{symbol}-{type}-{code}-"{except_msg}"')
        result = order_entrust_list(scene,endTime,forceClose,page,size,startTime,state,symbol,type)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')

        # try:
        args = {
            "col": "order",
        }
        # 未出现 error的场景
        if result.response.get("error") is None :
                # 返回结果有数据
                if result.response.get("result").get("items") != [] :
                    # 随机挑选一个测试数据
                    choice_res = random.choice(result.response.get("result").get("items"))
                    logger.info("choice_res : is {}".format(choice_res))
                    # 根据 订单Id 查询订单表
                    res = MongoDb(args).find({"_id":int(choice_res.get("id"))})
                    for i in res:
                        if float(choice_res.get("avgPrice")) != 0.0:
                            logger.info("mongo data {}".format(i))
                            # 价格
                            assert float(choice_res.get("avgPrice")) == float(i.get("avgPrice"))
                            # assert choice_res.get("type") == i.get("origType")
                            # 交易对
                            assert s.query.filter(s.symbol == '{}'.format(choice_res.get("symbol"))).first().id == i.get("symbolId")
                            # 订单来源
                            assert orderTypes.get(choice_res.get("orderType")) == i.get("orderType")
                            # 下单方向
                            assert orderSides.get(choice_res.get("orderSide")) == i.get("orderSide")
                            # 仓位模式
                            assert positionSides.get(choice_res.get("positionSide")) == i.get("positionSide")
                            # 有效方式
                            assert timeInForces.get(choice_res.get("timeInForce")) == i.get("timeInForce")
                            # 是否全部平仓，条件单使用
                            assert choice_res.get("closePosition") == i.get("closePosition")
                            # 数量
                            assert choice_res.get("origQty") == i.get("origQty")
                            # 占用保证金
                            assert float(choice_res.get("marginFrozen")) == float(i.get("marginFrozen"))
                            #订单状态
                            # 状态6是“EXPIRED"(已过期)（timeInForce撤单或者溢价撤单），为了满足产品需求给前端返回了一个"CANCELED"或者"PARTIALLY_CANCELED"方便前端展示的
                            assert choice_res.get("state") == "4" if i.get("state") == "6" else i.get("state")
                            assert choice_res.get("createdTime") == i.get("createdTime")

                     # 时间校验
                    if scene.endswith('根据startTime查找'):
                        # 随机选择一个 createdTime
                        createdTime = choice_res.get("createdTime")
                        # 根据 createdTime 作为参数
                        result_startTime_endTime_test = order_entrust_list(
                            scene, endTime, forceClose, page,size,createdTime, state, symbol, type)
                        for item in result_startTime_endTime_test.response.get("result").get("items"):
                            # 参数 createdTime 应该小于返回值的 createdTime
                            assert int(createdTime) <= int(item.get("createdTime"))
                        logger.info("根据startTime查找测试用例中,使用{}作为函数的createdTime".format(createdTime))

                    if scene.endswith('根据endTime查找'):
                        # 随机选择一个 createdTime
                        createdTime = choice_res.get("createdTime")
                        # 根据 createdTime 作为endTime参数
                        result_startTime_endTime_test = order_entrust_list(
                            scene, createdTime, forceClose, page, size, createdTime, state, symbol, type)
                        for item in result_startTime_endTime_test.response.get("result").get("items"):
                            # 返回值的 createdTime 应该小于 endTime参数
                            assert int(createdTime) >= int(item.get("createdTime"))
                        logger.info("根据endTime查找测试用例中,使用{}作为函数的endTime".format(createdTime))

                    if scene.endswith('endTime大于startTime') :
                        # 随机选择两个 createdTime
                        createdTime_1 = int(choice_res.get("createdTime"))
                        createdTime_2 = int(
                            random.choice(result.response.get("result").get("items")).get("createdTime"))
                        # 取 createdTime_1,createdTime_2 之中最大值为 endTime,最小值为startTime
                        result_startTime_endTime_test = order_entrust_list(
                            scene, max(createdTime_2, createdTime_1), forceClose, page, size,
                            min(createdTime_2, createdTime_1), state, symbol, type)
                        for item in result_startTime_endTime_test.response.get("result").get("items"):
                            # (createdTime > startTime) or (createdTime < endTime)
                            assert max(createdTime_2, createdTime_1) >= int(item.get("createdTime")) >= min(
                                createdTime_2, createdTime_1)
                            logger.info('endTime大于startTime测试用例中，endTime为{},startTime为{}'\
                                        .format(createdTime_1,createdTime_2))
                    if scene.endswith('endTime小于startTime'):
                        # 随机选择两个 createdTime
                        createdTime_1 = int(choice_res.get("createdTime"))
                        createdTime_2 = int(random.choice(result.response.get("result").get("items")).get("createdTime"))
                        # 取 createdTime_1,createdTime_2 之中最大值为 endTime,最小值为startTime
                        result_startTime_endTime_test = order_entrust_list(
                            scene, min(createdTime_2,createdTime_1), forceClose, page, size, max(createdTime_2,createdTime_1), state, symbol, type)
                        for item in result_startTime_endTime_test.response.get("result").get("items"):
                            # (createdTime > startTime) or (createdTime < endTime)
                            assert max(createdTime_2,createdTime_1) >= int(item.get("createdTime")) >= min(createdTime_2,createdTime_1)
                        logger.info('endTime小于startTime测试用例中，endTime为{},startTime为{}' \
                                    .format(max(createdTime_2,createdTime_1), min(createdTime_2,createdTime_1)))
        #   分页校验
        if page !="":
            if size != "":
                # 当前账户委托数据数量大于3才可以比较
                if len(result.response.get("result").get("items")) >= 3:
                    assert len(result.response.get("result").get("items")) == int(size)
                    assert result.response.get("result").get("page") == int(page)
                    assert result.response.get("result").get("ps") == int(size)
                    # page,size = (1, 2) 的最后一个值与 page,size = (2, 1)的第一个值相等
                    result_page_size_test = order_entrust_list(
                        scene, endTime, forceClose, 1, 2, startTime, state, symbol, type)
                    assert result.response.get("result").get("items")[0].get(id) == \
                          result_page_size_test.response.get("result").get("items")[-1].get(id)
                    logger.info("page,size = (1, 2) 的最后一个值与 page,size = (2, 1)的第一个值相等")

        # 状态值对比
        assert result.status_code == 200
        assert code == result.response["returnCode"]
        if code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "Test_order_entrust_list.py"])
