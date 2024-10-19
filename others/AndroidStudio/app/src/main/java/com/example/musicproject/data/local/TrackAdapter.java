package com.example.musicproject.data.local;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.musicproject.R;
import com.example.musicproject.domain.model.Result;

import java.io.File;
import java.util.List;

public class TrackAdapter  extends BaseAdapter {
    private Context context;
    private List<Result> items;

    public TrackAdapter(Context context, List<Result> items) {
        this.context = context;
        this.items = items;
    }

    @Override
    public int getCount() {
        return items.size();
    }

    @Override
    public Object getItem(int position) {
        return items.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    public static class ViewHolder {
        public ImageView imgArtWork;
        public TextView labTrackName;
        public TextView labArtistName;

        public ViewHolder(View view) {
            imgArtWork = (ImageView) view.findViewById(R.id.imgArtwork);
            labTrackName = (TextView) view.findViewById(R.id.labTrackName);
            labArtistName = (TextView) view.findViewById(R.id.lblArtistName);
        }
    }

    @Override
    public View getView(int pos, View convertView, ViewGroup parent) {
        final int ROW_RES = R.layout.row_view;
        ViewHolder viewHolder = null;

        if (convertView == null) {
            LayoutInflater layout = LayoutInflater.from(context);
            convertView = layout.inflate(ROW_RES, parent, false);
            viewHolder = new ViewHolder(convertView);
            convertView.setTag(viewHolder);
        } else {
            viewHolder = (ViewHolder) convertView.getTag();
        }

        Result res = items.get(pos);
        String fullFileName = context.getCacheDir() + "/"
                + res.getLocalArtworkFilename();
        if (new File(fullFileName).exists()) {
            Bitmap bm = BitmapFactory.decodeFile(fullFileName);
            viewHolder.imgArtWork.setImageBitmap(bm);
        } else {
            viewHolder.imgArtWork.setImageBitmap(null);
        }
        viewHolder.labTrackName.setText(res.getTrackName());
        viewHolder.labArtistName.setText(res.getArtistName());

        return convertView;
    }
}
