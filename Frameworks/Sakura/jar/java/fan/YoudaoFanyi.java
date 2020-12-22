package fan;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import okhttp3.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

public class YoudaoFanyi extends BaseFanyi implements BaseFanyi.RequestAPI {

    private static String cookies;
    String TAG = "有道";

    YoudaoFanyi() {
        super(2);
        api = this;
    }

    @Override
    public String getUrl() {
        return "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule";
    }

    @Override
    public RequestBody getBody() {
        String ts = String.valueOf(System.currentTimeMillis());
        String salt = String.valueOf((int) (System.currentTimeMillis() / 10));
        StringBuilder builder1 = new StringBuilder();
        try {
            MessageDigest m = MessageDigest.getInstance("MD5");
            StringBuilder builder = new StringBuilder("fanyideskweb");
            builder.append(text);
            builder.append(salt);
            builder.append("n%A-rKaT5fb[Gy?;N5@Tj");
            m.update(builder.toString().getBytes(StandardCharsets.UTF_8));
            byte s[] = m.digest();
            for (int i = 0; i < s.length; i++)
                builder1.append(Integer.toHexString((0x000000FF & s[i]) | 0xFFFFFF00).substring(6));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return new FormBody.Builder()
                .add("from", "auto")
                .add("to", "zh-CHS")
                .add("smartresult", "dict")
                .add("client", "fanyideskweb")
                .add("ts", ts)
                .add("bv", "53539dde41bde18f4a71bb075fcf2e66")
                .add("salt", salt)
                .add("sign", builder1.toString())
                .add("i", text)
                .add("doctype", "json")
                .add("version", "2.1")
                .add("keyfrom", "fanyi.web")
                .add("action", "FY_BY_CLICKBUTTION").build();
    }

    @Override
    public Headers getHeaders() {
        if (cookies == null)
            getSession();
        return new Headers.Builder()
                .add("Accept", "application/json, text/javascript, */*")
                .add("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
                .add("Host", "fanyi.youdao.com")
                .add("Origin", "http://fanyi.youdao.com")
                .add("Referer", "http://fanyi.youdao.com/")
                .add("Cookie", cookies)
                .add("X-Requested-With","XMLHttpRequest").build();
    }

    @Override
    public String getJson(String strings) {
        StringBuilder builder2 = new StringBuilder();
        for (Object object : (JSON.parseObject(strings).getJSONArray("translateResult").getJSONArray(0)))
            builder2.append(((JSONObject) object).getString("tgt"));
        return builder2.toString();
    }

    void getSession() {
        Headers headers = getBaseHeaders().add("Accept", "*/*")
                .add("Accept-Language", "zh-CN")
                .add("Content-Type", "charset=UTF-8")
                .add("Host", "fanyi.youdao.com").build();
        Request request = new Request.Builder().url("http://fanyi.youdao.com/").get().headers(headers).build();
        OkHttpClient client = new OkHttpClient.Builder().build();
        Call call = client.newCall(request);
        try {
            Response response = call.execute();
            Headers  header1 = response.headers();
            List<String> cookies = header1.values("Set-Cookie");
            StringBuilder builder = new StringBuilder();
            for (String cookie : cookies)
                builder.append(cookie);
            this.cookies = builder.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
    def translate(text, to='zhs', fr='ja'):
    global Cookie
    session = requests.session()
            try:
            if Cookie == "":

    ts = str(time.time() * 1000).split('.')[0]
    salt = str(int(ts) / 10).split('.')[0]
    md5s = hashlib.md5()
            md5s.update(("fanyideskweb" + text + salt + "n%A-rKaT5fb[Gy?;N5@Tj").encode('utf-8'))
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {'Host': 'fanyi.youdao.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, *//*',
            'Origin': 'https://fanyi.qq.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-495487002@10.169.0.83;JSESSIONID=aaa5vES2kUt0U_MqK3OWw',
            'Referer': 'http://fanyi.youdao.com/',
            'Accept-Encoding': 'gzip, deflate'}
    postData = {"from": "ja",
            "to": "zh-CHS",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "ts": ts,
            "bv": "53539dde41bde18f4a71bb075fcf2e66",
            "salt": salt,
            "sign": md5s.hexdigest(),
            "i": text,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION"}
    html2 = session.post(url=url, data=postData, headers=headers)
            if html2.ok:
    con = ''
            for strs in json.loads(html2.content)["translateResult"][0]:
    con += strs["tgt"]
            return con
        else:
    print ("error")
    **/

}
