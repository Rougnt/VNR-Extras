package fan;

import com.alibaba.fastjson.JSON;
import okhttp3.*;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.io.IOException;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class BaiduFanyi extends BaseFanyi implements BaseFanyi.RequestAPI {

    private static String cookies;
    private static String token;
    private static String gtk;
    String TAG = "百度";
    private static Invocable invoke;

    BaiduFanyi() throws ScriptException {
        super(0);
        api = this;
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("javascript");

        String JS_CODE = "function a(r, o) {\n" +
                "    for (var t = 0; t < o.length - 2; t += 3) {\n" +
                "        var a = o.charAt(t + 2);\n" +
                "        a = a >= \"a\" ? a.charCodeAt(0) - 87 : Number(a),\n" +
                "        a = \"+\" === o.charAt(t + 1) ? r >>> a: r << a,\n" +
                "        r = \"+\" === o.charAt(t) ? r + a & 4294967295 : r ^ a\n" +
                "    }\n" +
                "    return r\n" +
                "}\n" +
                "var C = null;\n" +
                "var token = function(r, _gtk) {\n" +
                "    var o = r.length;\n" +
                "    o > 30 && (r = \"\" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10));\n" +
                "    var t = void 0,\n" +
                "    t = null !== C ? C: (C = _gtk || \"\") || \"\";\n" +
                "    for (var e = t.split(\".\"), h = Number(e[0]) || 0, i = Number(e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) {\n" +
                "        var m = r.charCodeAt(g);\n" +
                "        128 > m ? d[f++] = m: (2048 > m ? d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128)\n" +
                "    }\n" +
                "    for (var S = h,\n" +
                "    u = \"+-a^+6\",\n" +
                "    l = \"+-3^+b+-f\",\n" +
                "    s = 0; s < d.length; s++) S += d[s],\n" +
                "    S = a(S, u);\n" +
                "    return S = a(S, l),\n" +
                "    S ^= i,\n" +
                "    0 > S && (S = (2147483647 & S) + 2147483648),\n" +
                "    S %= 1e6,\n" +
                "    S.toString() + \".\" + (S ^ h)\n" +
                "}";
        engine.eval(JS_CODE);

        invoke = (Invocable)engine;
    }

    @Override
    public String getUrl() {
        return "https://fanyi.baidu.com/v2transapi";
    }

    @Override
    public RequestBody getBody() {
        if (token == null || gtk == null)
            getToken();
        assert token != null;
        try {
            String sign = (String)invoke.invokeFunction("token", text, gtk);
            return new FormBody.Builder()
                    .add("from", "jp")
                    .add("to", "zh")
                    .add("query", text)
                    .add("transtype", "translang")
                    .add("simple_means_flag", "3")
                    .add("sign", sign)
                    .add("token", token).build();
        } catch (NoSuchMethodException | ScriptException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public Headers getHeaders() {
        if (cookies == null)
            getCookies();
        assert cookies != null;
        return getBaseHeaders().add("Accept", "*/*")
                .add("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
                .add("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
                .add("Cookie", cookies)
                .add("Host", "fanyi.baidu.com")
                .add("Origin", "https://fanyi.baidu.com")
                .add("Referer", "https://fanyi.baidu.com/?aldtype=16047")
                .add("X-Requested-With","XMLHttpRequest").build();
    }

    @Override
    public String getJson(String strings) {
        String string = JSON.parseObject(strings).getJSONObject("trans_result").getJSONArray("data").getJSONObject(0).getString("dst");
        return string;
    }

    private Response getSession(String host, String url) {
        Headers.Builder headers = getBaseHeaders().add("Accept", "*/*")
                .add("Accept-Language", "zh-CN")
                .add("Host", host);
        if (cookies != null)
            headers.add("Cookie", cookies);
        Request request = new Request.Builder().url(url).get().headers(headers.build()).build();
        OkHttpClient client = new OkHttpClient.Builder().build();
        Call call = client.newCall(request);
        try {
            return call.execute();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private void getCookies() {
        Response response = getSession("www.baidu.com", "https://www.baidu.com/");
        Headers header1 = response.headers();
        List<String> cookies = header1.values("Set-Cookie");
        StringBuilder builder = new StringBuilder();
        for (String cookie : cookies)
            builder.append(cookie);
        this.cookies = builder.toString();
    }

    private void getToken() {
        try {
            Response response = getSession("fanyi.baidu.com", "https://fanyi.baidu.com");
            String string = response.body().string();
            Pattern vPattern = Pattern.compile("token: \'\\S+\',");
            Matcher v = vPattern.matcher(string);
            while (v.find()) {
                String str = v.group();
                token = str.substring(8, str.length() - 2);
            }
            vPattern = Pattern.compile("window.gtk = \'\\S+\';");
            v = vPattern.matcher(string);
            while (v.find()) {
                String str = v.group();
                gtk = str.substring(14, str.length() - 2);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
