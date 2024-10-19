package com.example.musicproject;

import androidx.appcompat.app.AppCompatActivity;

import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;

import com.example.musicproject.data.local.TrackAdapter;
import com.example.musicproject.data.remote.AppleMusic;
import com.example.musicproject.domain.model.Result;
import com.example.musicproject.domain.model.Root;

import java.io.File;
import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    Button btnSearch;
    EditText txtSearchTerm;
    AppleMusic musicService;
    Root root;
    ListView livItems;
    private MediaPlayer mediaPlayer = null;
    private List<Result> results = null;

    private String currentFullFilename;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        musicService = new AppleMusic();
        results = new ArrayList<>();

        initViews();
        initEvents();
    }

    public void initViews(){
        livItems = findViewById(R.id.livTracks);
        txtSearchTerm = findViewById(R.id.txtSearchTerm);
        btnSearch = findViewById(R.id.btnSearch);

//        TrackAdapter adapter = new TrackAdapter(this, results);
//        livItems.setAdapter(adapter);
    }
    private void initEvents() {
        btnSearch.setOnClickListener(view -> {
            String term = txtSearchTerm.getText().toString().trim();

            // Detén la reproducción de cualquier track que se esté reproduciendo actualmente
            // stopTrack();

            musicService.requestSongsByTerm(term, 50, (root) -> {
                String cacheDir = getApplicationContext().getCacheDir().getAbsolutePath();

                this.root = root;
                // Descargar ilustraciones que faltan ejecutando tareas en segundo plano
                musicService.downloadArtworks(root, cacheDir);
                runOnUiThread(() -> {
                    // Actualiza la lista de pistas con los resultados
                     updateResultlist(root.getResults());
                });
            }, (errorCode, text) -> {
                runOnUiThread(() -> {
                    // Maneja los errores aquí, por ejemplo, mostrar un mensaje al usuario
                });
            });
        });
        livItems.setOnItemClickListener((adapterView, view, pos, l) -> {

            Result result = root.getResults().get(pos);
            String cacheDir = getApplicationContext().getCacheDir().getAbsolutePath();
            String filename = result.getLocalPreviewFilename();
            String fullFilename = cacheDir + "/" + filename;

            stopTrack(); // Mejorar

            if (new File(fullFilename).exists()) {
                playTrack(fullFilename);
                return;
            }
            musicService.downloadPreviewTrack(result, cacheDir, () -> {
                runOnUiThread(() -> {
                    playTrack(fullFilename);
                });
            }, (errorCode, text) -> {
            });
        });
    }

    public void stopTrack(){
        if (mediaPlayer != null){
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }
    public void playTrack(String fullFilename){
        stopTrack();
        File file = new File(fullFilename);
        if (!file.exists()) {
            // El archivo no existe
            Log.e("MediaPlayer", "El archivo de audio no existe: " + fullFilename);
            return;
        }
        Uri fileUri = Uri.fromFile(file);
        mediaPlayer = MediaPlayer.create(getApplicationContext(), fileUri);
        if (mediaPlayer != null) {
            try {
                mediaPlayer.start();
            } catch (IllegalStateException e) {
                Log.e("MediaPlayer", "Error al iniciar MediaPlayer", e);
                // Manejar la excepción
            }
        } else {
            Log.e("MediaPlayer", "No se pudo crear MediaPlayer para: " + fullFilename);
            // Manejar el caso de MediaPlayer.create() que devuelve null
        }
    }

    private void updateResultlist(List<Result> results){
        livItems.setAdapter(
            new TrackAdapter(getApplicationContext(),
            root.getResults())
        );
    }
}