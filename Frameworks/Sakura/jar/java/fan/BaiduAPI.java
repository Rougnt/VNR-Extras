package fan;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONException;
import okhttp3.Headers;
import okhttp3.RequestBody;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class BaiduAPI extends BaseFanyi implements BaseFanyi.RequestAPI {

    BaiduAPI() {
        super(0);
        api = this;
    }

    @Override
    public String getUrl() {
        long salt = System.currentTimeMillis();
        StringBuilder builder1 = new StringBuilder();
        try {
            MessageDigest m = MessageDigest.getInstance("MD5");
            StringBuilder builder = new StringBuilder(appid);
            builder.append(text);
            builder.append(salt);
            builder.append(key);
            m.update(builder.toString().getBytes(StandardCharsets.UTF_8));
            byte s[] = m.digest();
            for (int i = 0; i < s.length; i++)
                builder1.append(Integer.toHexString((0x000000FF & s[i]) | 0xFFFFFF00).substring(6));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        StringBuilder builder2 = new StringBuilder("http://api.fanyi.baidu.com/api/trans/vip/translate?q=");
        builder2.append(text);
        builder2.append("&from=auto&to=zh&appid=");
        builder2.append(appid);
        builder2.append("&salt=");
        builder2.append(salt);
        builder2.append("&sign=");
        builder2.append(builder1.toString());
        return builder2.toString();
    }

    @Override
    public RequestBody getBody() {
        return null;
    }

    @Override
    public Headers getHeaders() {
        return null;
    }

    @Override
    public String getJson(String strings) throws NullPointerException, JSONException {
        return JSON.parseObject(strings).getJSONArray("trans_result").getJSONObject(0).getString("dst");
    }

}
