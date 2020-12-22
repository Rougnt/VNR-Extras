package fan;

import javax.script.ScriptException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class Fanyi {

    static volatile String[] result = new String[4];
    private static BaiduFanyi baidu;
    private static BaiduAPI baiduapi = new BaiduAPI();
    private static TengxunFanyi tengxun = new TengxunFanyi();
    private static TengxunAPI tengxunapi = new TengxunAPI();
    private static YoudaoFanyi youdao = new YoudaoFanyi();
    private static CaiyunFanyi caiyun = new CaiyunFanyi();
    private static volatile CountDownLatch latch;

    public static void main(String main[]) throws ScriptException {
//      appid填 't' 是使用网页翻译，不填就是不启用翻译
        long start = System.currentTimeMillis();
        String s = "例え怪しいと分かっていても……何のスキルも持たない僕を愛してくれているのはエピデだけなんだ。聖女がいないと奇襲ができないじゃない。アレクたちは常人が歩くよりも遅い速度で必死に逃げるシャクトリに追い付いた。";
        translate(s, "t", "", "t", "", true, true);
        System.out.println(System.currentTimeMillis() - start);
        System.out.println(result[0]);
        System.out.println(result[1]);
        System.out.println(result[2]);
        System.out.println(result[3]);
    }

    public static synchronized String[] translate(String text, String appid1, String key1, String appid2, String key2, boolean b1, boolean b2) throws ScriptException {
        baidu = new BaiduFanyi();
        latch = new CountDownLatch(4);
        if (appid1.equals("t"))
            newThread(true, baidu.start(text, latch));
        else if (!appid1.equals(""))
            new Thread(baiduapi.start(text, appid1, key1, latch)).start();
        else
            latch.countDown();
        if (appid2.equals("t"))
            newThread(true, tengxun.start(text, latch));
        else if (!appid2.equals(""))
            new Thread(tengxunapi.start(text, appid2, key2, latch)).start();
        else
            latch.countDown();
        newThread(b1, youdao.start(text, latch));
        newThread(b2, caiyun.start(text, latch));
        try {
            latch.await(5000, TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static void newThread(boolean b, Runnable runnable) {
        if (b)
            new Thread(runnable).start();
        else
            latch.countDown();
    }

}
