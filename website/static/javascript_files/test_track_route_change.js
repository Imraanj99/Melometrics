function TestTopRouteChange(value) {
    // Construct the new URL path
    const newPath = `/test/top_tracks/${value}`;
    // Change the window's location
    window.location.pathname = newPath;
}