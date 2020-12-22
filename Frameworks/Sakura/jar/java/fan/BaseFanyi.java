package fan;

import com.alibaba.fastjson.JSONException;
import okhttp3.*;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class BaseFanyi implements Runnable {

    String text;
    int count = 0;
    RequestAPI api;
    CountDownLatch latch;
    OkHttpClient client;
    String appid;
    String key;
    Call call;

    BaseFanyi(int count) {
        this.count = count;
        client = new OkHttpClient.Builder().readTimeout(1666, TimeUnit.MILLISECONDS)
                .callTimeout(1666, TimeUnit.MILLISECONDS).writeTimeout(1666, TimeUnit.MILLISECONDS).build();
    }

    static Headers.Builder getBaseHeaders() {
        return new Headers.Builder()
                .add("Connection", "keep-alive")
                .add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36");
    }

    @Override
    public void run() {
        assert api != null;
        Headers headers = api.getHeaders();
        Request request = headers != null ? new Request.Builder().url(api.getUrl()).headers(headers).post(api.getBody()).build() :
                new Request.Builder().url(api.getUrl()).get().build();
        call = client.newCall(request);
        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                latch.countDown();
                Fanyi.result[count] = "翻译结果获取失败，连接超时";
                System.out.println(e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String string = response.body().string();
                if (string == null || string.isEmpty()) {
                    Fanyi.result[count] = "翻译结果获取失败，无内容返回";
                    latch.countDown();
                } else
                    try {
                        Fanyi.result[count] = api.getJson(string);
                    } catch (NullPointerException|JSONException e) {
                        Fanyi.result[count] = "翻译结果获取失败，请稍后再试，或更新版本";
                        System.out.println(e.getMessage());
                    } finally {
                        latch.countDown();
                    }
            }
        });
    }

    BaseFanyi start(String text, CountDownLatch latch) {
        if (call != null && call.isExecuted())
            call.cancel();
        this.text = text;
        this.latch = latch;
        return this;
    }

    BaseFanyi start(String text, String id, String key, CountDownLatch latch) {
        appid = id;
        this.key = key;
        return start(text, latch);
    }

    interface RequestAPI {

        String getUrl();

        RequestBody getBody();

        Headers getHeaders();

        String getJson(String strings) throws NullPointerException, JSONException, UnsupportedEncodingException;

    }
}
