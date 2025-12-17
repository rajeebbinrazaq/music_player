// Copyright (c) 2025, Music Player and contributors
// For license information, please see license.txt

frappe.ui.form.on("Music Playlist", {
    refresh(frm) {
        // Add custom button to play playlist
        if (!frm.is_new()) {
            frm.add_custom_button(__('Play Playlist'), function () {
                frappe.set_route('music-player', frm.doc.name);
            });
        }
    },
});
