package com.example.musicproject.data.remote;


import com.example.musicproject.domain.model.Result;
import com.example.musicproject.domain.model.Root;
import com.google.gson.Gson;

import java.io.File;

import cafsoft.foundation.HTTPURLResponse;
import cafsoft.foundation.URLComponents;
import cafsoft.foundation.URLQueryItem;
import cafsoft.foundation.URLRequest;
import cafsoft.foundation.URLSession;

public class AppleMusic {
    private final URLComponents components;

    public AppleMusic(){
        components = new URLComponents();
        components.setScheme("https");
        components.setHost("itunes.apple.com");
        components.setPath("/search");
    }

    public interface ErrorCodeCompletionHandler {
        void run(int errorCode, String text);
    }

    public interface RootCompletionHandler {
        void run(Root result);
    }

    public interface CompletionHandler {
        void run();
    }

    public void requestSongsByTerm(
            String searchTerm, int limit,
            RootCompletionHandler rootCompletion,
            ErrorCodeCompletionHandler errorCodeCompletion
    ) {
        components.setQueryItems(new URLQueryItem[]{
            new URLQueryItem("media",  "music"),
            new URLQueryItem( "entity", "song"),
            new URLQueryItem( "limit", String.valueOf(limit)),
            new URLQueryItem( "term", searchTerm)
        });

        // Generate the URL from the components
        var url = components.getURL();

        // Get Default URLSession
        var session = URLSession.getShared();

        // Create a network task for the GET request
        var task = session.dataTask(url, (data, response, error) -> {

            // Handle general errors
            if (error != null){
                // Network error
                errorCodeCompletion.run( -1, "");
                return;
            }

            if (response instanceof HTTPURLResponse){
                var httpResponse = (HTTPURLResponse) response;

                // process the received data
                var text = (data != null) ? data.toText() : "";
                var root = new Gson().fromJson(text, Root.class);

                // Check the status code
                if (httpResponse.getStatusCode() == 200){
                    if (rootCompletion != null){
                        rootCompletion.run(root);
                    }
                }else{
                    if (errorCodeCompletion != null){
                        errorCodeCompletion.run(httpResponse.getStatusCode(), text);
                    }
                }
            }
        });
        // Start the task
        task.resume();
    }

    public void downloadArtworks(Root root, String basePath) {
        if (root == null) {
            return;
        }
        for (Result result : root.getResults()) {
            var fullFilename = basePath + "/" + result.getLocalArtworkFilename();
            if (!new File(fullFilename).exists()) {
                // Initialize URLComponents
                var components = new URLComponents(result.getArtworkUrl100());
                // Create a URLRequest
                var request = new URLRequest(components.getURL());
                // Get Default URLSession
                var session = URLSession.getShared();
                // Create a network task for the download request
                var task = session.downloadTask(request, (localUrl, response, error) -> {
                    // Handle general errors
                    if (error != null) {
                        // Network error
                        return;
                    }
                    if (response instanceof HTTPURLResponse) {
                        var httpResponse = (HTTPURLResponse) response;
                        // Check the status code
                        if (httpResponse.getStatusCode() == 200) {
                            var file = new File(localUrl.getFile());

                            file.renameTo(new File(fullFilename));
                        }
                    }
                });
                // Start the task
                task.resume();
            }
        }
    }
    public void downloadPreviewTrack(
        Result result,
        String basePath,
        CompletionHandler completion,
        ErrorCodeCompletionHandler errorCodeCompletion
    ) {
        var fileFullName = basePath + "/" + result.getLocalPreviewFilename();
        URLComponents components = new URLComponents(result.getPreviewUrl());
        var url = components.getURL();

        var request = new URLRequest(components.getURL());
        var session = URLSession.getShared();

        var task = session.downloadTask(request, (localUrl, response, error) -> {
            if (error != null) {
                errorCodeCompletion.run(-1,"");
                return;
            }

            if (response instanceof HTTPURLResponse) {
                var httpResponse = (HTTPURLResponse) response;

                if(httpResponse.getStatusCode() == 200) {
                    var file = new File(localUrl.getFile());

                    file.renameTo(new File(fileFullName));
                    if(completion != null) {
                        completion.run();
                    }
                }else {
                    if(errorCodeCompletion !=  null) {
                        errorCodeCompletion.run(httpResponse.getStatusCode(), null);
                    }
                }
            }
        });
        task.resume();
    }
}