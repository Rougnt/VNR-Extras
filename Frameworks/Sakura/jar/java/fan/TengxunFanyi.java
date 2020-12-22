package fan;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import okhttp3.*;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TengxunFanyi extends BaseFanyi implements BaseFanyi.RequestAPI {

    private static String qtv;
    private static String qtk;
    String TAG = "腾讯";

    TengxunFanyi() {
        super(1);
        api = this;
    }

    private static void getQCode() {
        Headers headers = getBaseHeaders()
                .add("Accept", "*/*")
                .add("Content-Type", "charset=UTF-8").build();
        Request request = new Request.Builder().url("https://fanyi.qq.com/").get().headers(headers).build();
        OkHttpClient client = new OkHttpClient.Builder().build();
        try {
            Call call = client.newCall(request);
            Response response = call.execute();
            String strings = response.body().string();
            Pattern vPattern = Pattern.compile("var qtv = \"\\S+\";");
            Pattern kPattern = Pattern.compile("var qtk = \"\\S+\";");
            Matcher v = vPattern.matcher(strings);
            Matcher k = kPattern.matcher(strings);
            while (v.find()) {
                String str = v.group();
                qtv = str.substring(11, str.length() - 2);
            }
            while (k.find()) {
                String str = k.group();
                qtk = str.substring(11, str.length() - 2);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getUrl() {
        return "https://fanyi.qq.com/api/translate";
    }

    @Override
    public RequestBody getBody() {
        if (qtv == null)
            getQCode();
        StringBuilder builder = new StringBuilder("translate_uuid");
        builder.append(System.currentTimeMillis());
        return new FormBody.Builder()
                .add("source", "auto")
                .add("target", "zh")
                .add("sourceText", text)
                .add("qtv", qtv)
                .add("qtk", qtk)
                .add("sessionUuid", builder.toString()).build();
    }

    @Override
    public Headers getHeaders() {
        return getBaseHeaders().add("Accept", "application/json, text/javascript, */*")
                .add("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
                .add("Host", "fanyi.qq.com")
                .add("Origin", "https://fanyi.qq.com")
                .add("Referer", "https://fanyi.qq.com/")
                .add("X-Requested-With","XMLHttpRequest").build();
    }

    @Override
    public String getJson(String strings) {
        StringBuilder builder1 = new StringBuilder();
        for (Object object : (JSON.parseObject(strings).getJSONObject("translate").getJSONArray("records")))
            builder1.append(((JSONObject) object).getString("targetText"));
        return builder1.toString();
    }
/**

    def translate(text, to='zhs', fr='ja'):
    session = requests.session()
            if len(qtv) == 0:
    get_qt_code()
    try:
    url = 'https://fanyi.qq.com/api/translate'
    headers = {'Host': 'fanyi.qq.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, *//*',
            'Origin': 'https://fanyi.qq.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://fanyi.qq.com/',
                'Accept-Encoding': 'gzip, deflate, br'}
    data = {"source": "jp",
            "target": "zh",
            "sourceText": text,
            "qtv": qtv,
            "qtk": qtk,
            "sessionUuid": 'translate_uuid' + str(time.time() * 1000).split('.')[0]}

    html2 = session.post(url=url, data=data, headers=headers)
            if html2.ok:
    con = ''
            for strs in json.loads(html2.content)["translate"]["records"]:
    con += strs["targetText"]
            if con.encode("utf-8") == "。" or con.encode("utf-8") == "":
    get_qt_code()
    con = translate(text)
            return con
        else:
    print ("error")
            **/
}
