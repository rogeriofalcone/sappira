CDC Percentile Data

^([\d]+)\t([\d]+)\t([\d]+)\t([\d\.\d]+)\t([\d\.\d]+)\t([\d\.\d]+)\t([\d\.\d]+)\t([\d\.\d]+)\t([\d\.\d]+)

<object pk="$1" model="sentinel.cdc_percentile">
\t<field type="IntegerField" name="gender">$2</field>
\t<field type="FloatField" name="age_in_months">$3</field>
\t<field type="FloatField" name="weight_cox">$4</field>
\t<field type="FloatField" name="weight_median">$5</field>
\t<field type="FloatField" name="weight_variation">$6</field>
\t<field type="FloatField" name="height_cox">$7</field>
\t<field type="FloatField" name="height_median">$8</field>
\t<field type="FloatField" name="height_variation">$8</field>
</object>

FDA Drug List

^([\w\.]+)\t(.+)

<object pk="$1" model="sentinel.fda_drug_data">
	\t<field type="CharField" name="drug_name">$2</field>
</object>

ICD-10 to Tab Delimited

^([\A-Z]+)([\d]+\.[\d]+)(.+)

$1\t$2\t$3

ICD-10 Erase Post Newline Spaces
\n^[\s]+

\n

ICD-10 To Fixture

^([0-9]+)\t([\A-Z]+)\t([\d\.\d]+)\t(.+)

<object pk="$1" model="sentinel.problem">
\t<field type="CharField" name="code">$2$3</field>
\t<field type="CharField" name="name">$4</field>
</object>

<button class="add-button" onClick="$.post("/presciption/add/", $("#prescription-{{ patient.id }}").serialize());">Add</button>

$("#prescription-list li").draggable({ revert: true });
$("#problem-list li").droppable({
	hoverClass: "highlight",
	drop: function( event, ui ) {
		$(this)
			.effect("highlight")
			.next(".details").append("<li>" + ui.draggable.text() + "</li>")
			.show()
	}
});



background: #eceef3;

function percentile_from_zscore(z) {
    var y, x, w;
    
    if (z == 0.0) {
        x = 0.0;
    } 
	
	else {
		y = 0.5 * Math.abs(z);
       	if (y > (6 * 0.5)) {
            x = 1.0;
        } else if (y < 1.0) {
            w = y * y;
            x = ((((((((0.000124818987 * w
                     - 0.001075204047) * w + 0.005198775019) * w
                     - 0.019198292004) * w + 0.059054035642) * w
                     - 0.151968751364) * w + 0.319152932694) * w
                     - 0.531923007300) * w + 0.797884560593) * y * 2.0;
        } else {
            y -= 2.0;
            x = (((((((((((((-0.000045255659 * y
                           + 0.000152529290) * y - 0.000019538132) * y
                           - 0.000676904986) * y + 0.001390604284) * y
                           - 0.000794620820) * y - 0.002034254874) * y
                           + 0.006549791214) * y - 0.010557625006) * y
                           + 0.011630447319) * y - 0.009279453341) * y
                           + 0.005353579108) * y - 0.002141268741) * y
                           + 0.000535310849) * y + 0.999936657524;
        }
    }
    return z > 0.0 ? ((x + 1.0) * 0.5)*100 : ((1.0 - x) * 0.5)*100;
}

function calculate_lms_percentile(value, median, variation, cox) {
	var z_score = (Math.pow((value/median),cox)-1)/(cox*variation);
	return Math.round(percentile_from_zscore(z_score)*10)/10;
}

function calculate_weight_percentile(gender, age_in_months, weight) {
	$.get('/percentile/', { gender:gender, age_in_months:age_in_months }, function(json_data) {
		$('#id_weight_percentile').val(calculate_lms_percentile(weight, json_data[0].fields.weight_median, json_data[0].fields.weight_variation, json_data[0].fields.weight_cox));
	});
}

function calculate_height_percentile(gender, age_in_months, height) {
	$.get('/percentile/', { gender:gender, age_in_months:age_in_months }, function(json_data) {
		$('#id_height_percentile').val(calculate_lms_percentile(height, json_data[0].fields.height_median, json_data[0].fields.height_variation, json_data[0].fields.height_cox));
	});
}