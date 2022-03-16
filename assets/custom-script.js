const LABEL_COLOR = 'rgb(42, 63, 95)'

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        feature_search: function(search_text) {
            reset_all_feature_labels(LABEL_COLOR);
            highlight_matching_labels(search_text);
            return 'DUMMY';
        }
    }
});

function reset_all_feature_labels(color) {
    for (const node of get_all_feature_labels()) {
        node.style.fontWeight = 'normal';
        node.style.fill = color;
    }
}


function get_all_feature_labels() {
    let xpath = '//*[name()="svg" and @class="main-svg"][1]'
        + '//*[name()="g" and @class="ytick"]/*[name()="text"]'
    let all_labels = []
    result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null)
    while (node = result.iterateNext()) {
        all_labels.push(node);
    }
    return all_labels;
}


function highlight_matching_labels(search_text) {
    for (const node of get_matching_labels(search_text)) {
        node.style.fontWeight = 'bold';
        node.style.fill = 'orangered';
    }
}


function get_matching_labels(search_text) {
    if (search_text === "") {
        return []
    }
    let xpath = '//*[name()="svg" and @class="main-svg"][1]'
        + '//*[name()="g" and @class="ytick"]/*[name()="text"]'
        + '[contains(text(), "' + search_text + '")]'
    let matching_labels = []
    result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null)
    while (node = result.iterateNext()) {
        matching_labels.push(node);
    }
    return matching_labels;
}
