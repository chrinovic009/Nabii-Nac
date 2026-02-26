$(document).ready(function() {

    $('#countdown').countdown('2026/03/30 00:00:00', function(event) {

        $('#days').text(event.offset.totalDays.toString().padStart(2, "0"));
        $('#hours').text(event.offset.hours.toString().padStart(2, "0"));
        $('#minutes').text(event.offset.minutes.toString().padStart(2, "0"));
        $('#seconds').text(event.offset.seconds.toString().padStart(2, "0"));

    });

});

$(document).ready(function(){

    $('.course-slider').owlCarousel({
        items: 1,
        loop: true,
        margin: 0,
        nav: true,
        dots: false,
        smartSpeed: 800,
        autoHeight: true,
        navText: [
            '<i class="fa fa-chevron-left"></i>',
            '<i class="fa fa-chevron-right"></i>'
        ]
    });

});

$(document).ready(function() {
    var postsPerPage = 2; // nombre de posts à afficher par page
    var $posts = $('.post-item'); // tous les posts
    var currentPage = 0;
    var totalPages = Math.ceil($posts.length / postsPerPage);

    // 1️⃣ Générer automatiquement les numéros de page
    var $pagination = $('.site-pageination');
    $pagination.find('.page-number').remove(); // supprimer les numéros existants si présents
    for (var i = 0; i < totalPages; i++) {
        $('<li><a href="#" class="page-number" data-page="'+i+'">'+(i+1)+'</a></li>')
            .insertBefore($pagination.find('.page-next'));
    }

    function showPage(page) {
        $posts.hide();
        var start = page * postsPerPage;
        var end = start + postsPerPage;
        $posts.slice(start, end).show();
        currentPage = page;

        // mettre à jour les numéros actifs
        $('.page-number').removeClass('active');
        $('.page-number[data-page="' + page + '"]').addClass('active');
    }

    // clic sur numéro de page
    $(document).on('click', '.page-number', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        showPage(page);
    });

    // clic flèche droite
    $('.page-next').click(function(e) {
        e.preventDefault();
        if(currentPage + 1 < totalPages){
            showPage(currentPage + 1);
        }
    });

    // clic flèche gauche
    $('.page-prev').click(function(e) {
        e.preventDefault();
        if(currentPage > 0){
            showPage(currentPage - 1);
        }
    });

    // afficher la première page par défaut
    showPage(0);
});

$(document).ready(function(){

    function setBg(){
        $(".set-bg").each(function(){
            var bg = $(this).data("setbg");
            $(this).css("background-image","url("+bg+")");
        });
    }

    setBg();

    var enqueteSlider = $(".enquete-slider");

    enqueteSlider.owlCarousel({
        items:1,
        loop:true,
        margin:30,
        nav:true,
        dots:true,
        autoplay:true,
        autoplayTimeout:5000,
        autoHeight:true, // <-- uniformise la hauteur
        navText:[
            "<i class='fa fa-angle-left'></i>",
            "<i class='fa fa-angle-right'></i>"
        ]
    });

    function initMasonry(){
        $('.gallery').each(function(){
            var $grid = $(this);
            $grid.imagesLoaded(function(){
                $grid.masonry({
                    itemSelector: '.gallery-item',
                    columnWidth: '.grid-sizer',
                    percentPosition: true
                });
            });
        });
    }

    // lancement initial après init Owl
    enqueteSlider.on('initialized.owl.carousel', function () {
        setBg();
        initMasonry();
    });

    // recalcul quand le slide change
    enqueteSlider.on('changed.owl.carousel', function () {
        setBg();
        setTimeout(function(){
            initMasonry();
        }, 300);
    });

});
