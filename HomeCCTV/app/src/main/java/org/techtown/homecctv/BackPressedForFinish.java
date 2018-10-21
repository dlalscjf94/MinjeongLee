package org.techtown.homecctv;

import android.app.Activity;
import android.widget.Toast;

public class BackPressedForFinish {
    private long backKeyPressedTime = 0;
    private long TIME_INTERVAL = 2000;
    private Toast toast;
    private Activity activity;

    public BackPressedForFinish(Activity _activity) {
        this.activity = _activity;
    }

    public void onBackPressed(MyClientTask cl) {

        if (System.currentTimeMillis() > backKeyPressedTime + TIME_INTERVAL) {

            backKeyPressedTime = System.currentTimeMillis();
            showMessage();

        }else{

            toast.cancel();

            cl.execute();
            activity.finish();
        }
    }

    public void showMessage() {
        toast = Toast.makeText(activity, "'뒤로' 버튼을 한번 더 누르시면 종료됩니다.", Toast.LENGTH_SHORT);
        toast.show();
    }
}
