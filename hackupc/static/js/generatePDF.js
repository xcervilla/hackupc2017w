/**
 * Created by xavier on 4/3/17.
 */

function generatePDF() {
    $.ajax({
        type:"GET",
        url:"/proposals/getPDFData/"+ proposal_pk + '/',
        dataType: 'json',
        success: function (d) {

            var doc = new jsPDF();
            doc.text('Title of the proposal: ' + proposal_title, 10, 10);
            doc.text('ID Nº', 10, 20);
            doc.text('Name', 50, 20);
            doc.text('Surname', 80, 20);
            doc.text('Signature', 150, 20);
            var h = 30;
            console.log(d);
            for(var i=0; i < d.a.length ; ++i){
                doc.text(d.a[i].id, 10, h);
                doc.text(d.a[i].name, 50, h);
                doc.text(d.a[i].surname, 80, h);
                console.log(d.a[i].signature);
                doc.addImage(d.a[i].signature,'jpeg',150,h,30,20);
                h += 30
            }
            doc.save(proposal_title +'.pdf');
        }
    });

}
