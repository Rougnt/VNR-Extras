package fan;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONException;
import okhttp3.Headers;
import okhttp3.RequestBody;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.bind.DatatypeConverter;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

public class TengxunAPI extends BaseFanyi implements BaseFanyi.RequestAPI {

    private final static String CHARSET = "UTF-8";

    TengxunAPI() {
        super(1);
        api = this;
    }

    private String sign(String s, String key, String method) throws Exception {
        Mac mac = Mac.getInstance(method);
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(CHARSET), mac.getAlgorithm());
        mac.init(secretKeySpec);
        byte[] hash = mac.doFinal(s.getBytes(CHARSET));
        return DatatypeConverter.printBase64Binary(hash);
    }

    private String getStringToSign(String id, String text) throws UnsupportedEncodingException {
        // 签名时要求对参数进行字典排序
        StringBuilder s2s = new StringBuilder("GETtmt.tencentcloudapi.com/?Action=TextTranslate&Nonce=11186&ProjectId=0&Region=ap-guangzhou&SecretId=");
        s2s.append(id);
        s2s.append("&Source=auto&SourceText=");
        s2s.append(text);
        s2s.append("&Target=zh&Timestamp=");
        s2s.append(System.currentTimeMillis() / 1000);
        s2s.append("&Version=2018-03-21");
        return s2s.toString();
    }

    @Override
    public String getUrl() {
        try {
            StringBuilder builder = new StringBuilder("https://");
            builder.append(getStringToSign(appid, URLEncoder.encode(text, "utf-8")).substring(3));
            builder.append("&Signature=");
            builder.append(URLEncoder.encode(sign(getStringToSign(appid, text), key, "HmacSHA1"), "utf-8"));
            return builder.toString();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return "";
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
    public String getJson(String strings) throws NullPointerException, JSONException, UnsupportedEncodingException {
        return JSON.parseObject(strings).getJSONObject("Response").getString("TargetText");
    }
}
