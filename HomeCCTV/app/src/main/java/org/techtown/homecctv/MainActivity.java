package org.techtown.homecctv;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    Button Btn;
    EditText Edit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Btn = (Button) findViewById(R.id.button);
        Edit = (EditText) findViewById(R.id.editText);
    }

    public void onButtonClicked(View v){
        String IP = Edit.getText().toString();
        Intent intent = new Intent(getApplicationContext(), ViewActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("IP",IP);
        intent.putExtras(bundle);
        startActivity(intent);
        finish();
    }
}
