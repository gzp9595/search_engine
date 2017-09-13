/**
 * Author: Ying Lin
 * Date: Sep 01, 2017
 */
var MAX_LENGTH_QUERY = 100;
var MAX_LENGTH_NAME_OF_CASE = 50;
var MAX_LENGTH_CASE_NUMBER = 50;
var MAX_LENGTH_NAME_OF_COURT = 50;
var MAX_LENGTH_NAME_OF_LAW = 50;
var MAX_LENGTH_ARTICLE = 50;
var MAX_LENGTH_PARAGRAPH = 50;
var SEARCH_URL = 'http://bc2.citr.me:8000/search';
$(document).ready(function () {

})
    .on('click', '#search-advance-expand', advance_search_toggle)
    .on('click', '#search-button', search);

/**
 * Adjust
 * @param e
 */
function textarea_auto_grow(e) {
    e.style.height = '5px';
    e.style.height = (e.scrollHeight) + 'px';
}

/**
 * Toggle advanced search options
 */
function advance_search_toggle() {
    $('#search-advance').toggleClass('expand');
}

/**
 * Get search parameters from form
 */
function get_parameters() {
    var parameters = {valid: true};
    var type_of_model = $('select[name="type_of_model"]').val();
    parameters.type_of_model = type_of_model;
    // basic search
    var query = $('#search-input').val();
    if (typeof query !== 'undefined') {
        query = query.trim();
        if (query.length > 0 && query.length < MAX_LENGTH_QUERY) {
            parameters.search_content = query;
        } else {
            parameters.valid = false;
            return parameters;
        }
    } else {
        parameters.valid = false;
        return parameters;
    }

    // advanced search
    // case name
    var name_of_case = $('input[name="name_of_case"]').val();
    if (typeof name_of_case !== 'undefined' && name_of_case.length !== 0) {
        name_of_case = name_of_case.trim();
        if (name_of_case.length > 0 && name_of_case.length < MAX_LENGTH_NAME_OF_CASE) {
            parameters.name_of_case = name_of_case;
        }
    }
    // case number
    var case_number = $('input[name="case_number"]').val();
    if (typeof case_number !== 'undefined' && case_number.length !== 0) {
        case_number = case_number.trim();
        if (case_number.length > 0 && case_number.length < MAX_LENGTH_CASE_NUMBER) {
            parameters.case_number = case_number;
        }
    }
    // name of court
    var name_of_court = $('input[name="name_of_court"]').val();
    if (typeof name_of_court !== 'undefined' && name_of_court.length !== 0) {
        name_of_court = name_of_court.trim();
        if (name_of_court.length > 0 && name_of_court.length < MAX_LENGTH_NAME_OF_COURT) {
            parameters.case_number = name_of_court;
        }
    }
    // level of court
    var level_of_court = $('select[name="level_of_court"]').val();
    if (typeof level_of_court !== 'undefined' && level_of_court.length !== 0) {
        parameters.level_of_court = level_of_court;
    }
    // type of case
    var type_of_case = $('select[name="type_of_case"]').val();
    if (typeof type_of_case !== 'undefined' && type_of_case.length !== 0) {
        parameters.type_of_case = type_of_case;
    }
    // type of doc
    var type_of_doc = $('select[name="type_of_doc"]').val();
    if (typeof type_of_doc !== 'undefined' && type_of_doc.length !== 0) {
        parameters.type_of_doc = type_of_doc;
    }
    // judge date
    var judge_date_from = $('input[name="judge_date_from"]').val();
    var judge_date_to = $('input[name="judge_date_to"]').val();
    if (typeof judge_date_from !== 'undefined' && typeof judge_date_to !== 'undefined'
    && judge_date_from.length !== 0 && judge_date_to.length !== 0) {
        var judge_date_from_segs = judge_date_from.split('-');
        var judge_date_to_segs = judge_date_to.split('-');
        if (judge_date_from_segs.length === 3 && judge_date_to_segs.length === 3) {
            var judge_date_from_year = judge_date_from_segs[0];
            var judge_date_from_month = judge_date_from_segs[1];
            var judge_date_from_day = judge_date_from_segs[2];
            var judge_date_to_year = judge_date_to_segs[0];
            var judge_date_to_month = judge_date_to_segs[1];
            var judge_date_to_day = judge_date_to_segs[2];
            try {
                judge_date_from_year = parseInt(judge_date_from_year);
                judge_date_from_month = parseInt(judge_date_from_month);
                judge_date_from_day = parseInt(judge_date_from_day);
                judge_date_to_year = parseInt(judge_date_to_year);
                judge_date_to_month = parseInt(judge_date_to_month);
                judge_date_to_day = parseInt(judge_date_to_day);
                parameters.caipan_from_year = judge_date_from_year;
                parameters.caipan_from_month = judge_date_from_month;
                parameters.caipan_from_day = judge_date_from_day;
                parameters.caipan_to_year = judge_date_to_year;
                parameters.caipan_to_month = judge_date_to_month;
                parameters.caipan_to_day = judge_date_to_day;
            } catch (err) {
                console.log(err);
            }
        }
    }
    // judgement
    // var judgement = $('select[name="judgement"]').val();
    // if (typeof judgement !== 'undefined' && judgement.length !== 0) {
    //     parameters.judgement = judgement;
    // }
    // name of law
    var name_of_law = $('input[name="name_of_law"]').val();
    if (typeof name_of_law !== 'undefined' && name_of_law.length !== 0) {
        name_of_law = name_of_law.trim();
        if (name_of_law.length > 0 && name_of_law.length < MAX_LENGTH_NAME_OF_LAW) {
            parameters.name_of_law = name_of_law;
        }
    }
    // article
    var article = $('input[name="article"]').val();
    if (typeof article !== 'undefined' && article.length !== 0) {
        article = article.trim();
        if (article.length > 0 && article.length < MAX_LENGTH_ARTICLE) {
            parameters.name_of_tiao = article;
        }
    }
    // paragraph
    var paragraph = $('input[name="paragraph"]').val();
    if (typeof paragraph !== 'undefined' && paragraph.length !== 0) {
        paragraph = paragraph.trim();
        if (paragraph.length > 0 && paragraph.length < MAX_LENGTH_PARAGRAPH) {
            parameters.name_of_kuan = paragraph;
        }
    }
    // publication date
    var publication_date_from = $('input[name="publication_date_from"]').val();
    var publication_date_to = $('input[name="publication_date_to"]').val();
    if (typeof publication_date_from !== 'undefined' && typeof publication_date_to !== 'undefined'
    && publication_date_from.length !== 0 && publication_date_to.length !== 0) {
        var publication_date_from_segs = publication_date_from.split('-');
        var publication_date_to_segs = publication_date_to.split('-');
        if (publication_date_from_segs.length === 3 && publication_date_to_segs.length === 3) {
            var publication_date_from_year = publication_date_from_segs[0];
            var publication_date_from_month = publication_date_from_segs[1];
            var publication_date_from_day = publication_date_from_segs[2];
            var publication_date_to_year = publication_date_to_segs[0];
            var publication_date_to_month = publication_date_to_segs[1];
            var publication_date_to_day = publication_date_to_segs[2];
            try {
                publication_date_from_year = parseInt(publication_date_from_year);
                publication_date_from_month = parseInt(publication_date_from_month);
                publication_date_from_day = parseInt(publication_date_from_day);
                publication_date_to_year = parseInt(publication_date_to_year);
                publication_date_to_month = parseInt(publication_date_to_month);
                publication_date_to_day = parseInt(publication_date_to_day);
                parameters.fabu_from_year = publication_date_from_year;
                parameters.fabu_from_month = publication_date_from_month;
                parameters.fabu_from_day = publication_date_from_day;
                parameters.fabu_to_year = publication_date_to_year;
                parameters.fabu_to_month = publication_date_to_month;
                parameters.fabu_to_day = publication_date_to_day;
            } catch (err) {
                console.log(err);
            }
        }
    }

    return parameters;
}

function search() {
    var parameters = get_parameters();
    if (parameters.valid) {
        parameters.where_to_search = 0;
        parameters.index = 'law';
        parameters.doc_type = 'big_data';
        delete parameters.valid;
        // $.ajax({
        //     url: '/search',
        //     data: parameters
        // }).done(function (data) {
        //     console.log(data)
        // });
        window.location.href = "/search?" + $.param(parameters);
    } else {
        // error
    }
}

function load_document() {

}