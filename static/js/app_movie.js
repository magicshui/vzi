Movies = Ember.Application.Create();

Movies.Info = Em.Object.extend({
    title:'',
    image:'',
    alt_title:'',
    summary:'',
    id:''
});

Movies.Line = Em.Object.extend({
   name:'',
   avatar:'',
    content:'',
    crt_time:null,
    line_id:''
});

Movies.linesController = Em.ArrayProxy.create({

});