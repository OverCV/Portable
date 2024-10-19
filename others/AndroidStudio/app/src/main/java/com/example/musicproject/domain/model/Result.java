package com.example.musicproject.domain.model;

public class Result {
    private long collectionId = 0;
    private long trackId = 0;
    private String artistName = "";
    private String trackName = "";
    private String previewUrl = "";
    private String artworkUrl100 = "";
    public long getCollectionId() {
        return collectionId;
    }
    public long getTrackId() {
        return trackId;
    }
    public String getArtistName() {
        return artistName;
    }
    public String getTrackName() {
        return trackName;
    }
    public String getPreviewUrl() {
        return previewUrl;
    }
    public String getArtworkUrl100() {
        return artworkUrl100;
    }
    public String getLocalPreviewFilename(){
        return getTrackId() + ".m4a.tmp";
    }
    public String getLocalArtworkFilename(){
        return getCollectionId() + ".jpg.tmp";
    }
}
