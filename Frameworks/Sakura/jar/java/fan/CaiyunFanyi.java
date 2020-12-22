package fan;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import okhttp3.*;

public class CaiyunFanyi extends BaseFanyi implements BaseFanyi.RequestAPI {

    String TAG = "彩云";

    CaiyunFanyi() {
        super(3);
        api = this;
    }

    @Override
    public String getUrl() {
        return "https://api.interpreter.caiyunai.com/v1/translator";
    }

    @Override
    public RequestBody getBody() {
        JSONObject object = new JSONObject();
        object.put("source", text);
        object.put("trans_type", "ja2zh");
        object.put("request_id", "web_fanyi");
        object.put("media", "text");
        object.put("os_type", "web");
        object.put("dict", "false");
        object.put("cached", "false");
        object.put("replaced", "false");
        return RequestBody.create(MediaType.parse("application/json; charset=utf-8"), object.toString());
    }

    @Override
    public Headers getHeaders() {
        return getBaseHeaders().add("Accept", "application/json, text/plain, */*")
                .add("Content-Type", "application/json;charset=UTF-8")
                .add("Origin", "https://fanyi.caiyunapp.com")
                .add("Referer", "https://fanyi.caiyunapp.com/")
                .add("X-Authorization","token 3975l6lr5pcbvidl6jl2").build();
    }

    @Override
    public String getJson(String strings) {
        return JSON.parseObject(strings).getString("target");
    }
}
