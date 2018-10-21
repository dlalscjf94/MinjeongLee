package org.techtown.homecctv;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.Toast;

import java.net.Socket;

public class ViewActivity extends AppCompatActivity {

    private BackPressedForFinish backPressedForFinish;

    Button upBtn, downBtn, leftBtn, rightBtn, centerBtn, on, off;

    Socket socket = null;
    String addr;
    int port = 8888;

    MyClientTask myClientTask;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        String IP = bundle.getString("IP");

        addr = IP;

        // BackPressedForFinish 객체를 생성한다.
        backPressedForFinish = new BackPressedForFinish(this);

        upBtn = (Button) findViewById(R.id.button);
        downBtn = (Button) findViewById(R.id.button2);
        leftBtn = (Button) findViewById(R.id.button3);
        rightBtn = (Button) findViewById(R.id.button4);
        centerBtn = (Button) findViewById(R.id.button5);
        on = (Button) findViewById(R.id.button7);
        off = (Button) findViewById(R.id.button8);

        String url = "http://"+IP+":5000/video_feed";

        WebView webView = (WebView) findViewById(R.id.webView);
        webView.setWebViewClient(new WebViewClient());

        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        webView.loadUrl(url);

        myClientTask = new MyClientTask(addr,port,"start");
        myClientTask.execute();

        upBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"up");
                myClientTask.execute();
            }
        });

        downBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"down");
                myClientTask.execute();
            }
        });

        leftBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"left");
                myClientTask.execute();
            }
        });

        rightBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"right");
                myClientTask.execute();
            }
        });

        centerBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"center");
                myClientTask.execute();
            }
        });

        on.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"on");
                myClientTask.execute();
                Toast.makeText(getApplicationContext(), "Auto on", Toast.LENGTH_LONG).show();
            }
        });

        off.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                myClientTask = new MyClientTask(addr,port,"off");
                myClientTask.execute();
                Toast.makeText(getApplicationContext(), "Auto off", Toast.LENGTH_LONG).show();
            }
        });
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        System.exit(0);
    }

    @Override
    public void onBackPressed() {
        myClientTask = new MyClientTask(addr,port,"end");
        // BackPressedForFinish 클래스의 onBackPressed() 함수를 호출한다.
        backPressedForFinish.onBackPressed(myClientTask);
    }
}
