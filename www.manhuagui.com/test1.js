window.alert("test")
var tes = {c:function(){}}
tes.c = function() {
    window.alert("IN");
    return function(n) {
        function s(n) {
            return 's' + n;
        }
        return window.alert("tes1"),{
            init: function() {
                return "innt" + n;
            },
            print: function(n) {
                return 'p' + n;
            },
        }
    }
}();