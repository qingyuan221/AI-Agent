import asyncio
import time
from openai import AsyncOpenAI
#1.初始化异步客户端
client = AsyncOpenAI(
    api_key="1bf7ef3239fc4649825b4673e5731211.zamL3TFjqwMb2Tfy",
    base_url="https://open.bigmodel.cn/api/paas/v4"

)
async def fetch_movie_summary(movie_name:str):
    """
    异步获取单部电影介绍
    """
    start_time = time.perf_counter()
    print(f"开始获取《{movie_name}》的信息...")
    try:
        response = await client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role":"system","content":"你是一个电影专家，简要介绍一下这部电影的剧情。"},
                {"role":"user","content":f"请介绍一下《{movie_name}》这部电影。"}
            ],
            stream=False#并发模式下，等待全部完成后统一展示
        )
        reply = response.choices[0].message.content
        end_time = time.perf_counter()
        print(  f"获取《{movie_name}》信息完成，耗时 {end_time - start_time:.2f} 秒")
        return f"《{movie_name}》{reply}"
    except Exception as e:
        return f"获取《{movie_name}》信息失败: {e}"
async def main():
        movies = ["盗梦空间", "阿凡达", "泰坦尼克号"]
        total_start = time.perf_counter()
        print("=====并发请求测试开始=====")
        #2.创建任务列表
        tasks = [fetch_movie_summary(m) for m in movies]
        #3.使用asyncio.gather并发执行所有任务
        results = await asyncio.gather(*tasks)
        print("\n" + "="*30)
        print("最终对比结果:")
        for res in results:
            print(res)
        total_end = time.perf_counter()
        print("="*30)
        print(f"=====并发请求测试结束，总耗时 {total_end - total_start:.2f} 秒=====")
if __name__ == "__main__":
    asyncio.run(main())