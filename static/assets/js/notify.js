const notify = (title, message, type) => {
    var placementFrom = "top";
    var placementAlign = "right";
    var state = type;
    var content = {};

    content.message = message;
    content.title = title + " ";
    content.icon = "fa fa-bell";

    $.notify(content, {
        type: state,
        placement: {
            from: placementFrom,
            align: placementAlign,
        },
        time: 1000,
        delay: 0,
    });
};
