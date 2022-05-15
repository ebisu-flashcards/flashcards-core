Search.setIndex({docnames:["database","index","models","schedulers","study"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["database.rst","index.rst","models.rst","schedulers.rst","study.rst"],objects:{"flashcards_core.database":[[0,0,0,"-","crud"],[0,0,0,"-","exporter"],[0,0,0,"-","importer"],[0,4,1,"","init_db"]],"flashcards_core.database.crud":[[0,1,1,"","CrudOperations"]],"flashcards_core.database.crud.CrudOperations":[[0,2,1,"","create"],[0,2,1,"","create_async"],[0,2,1,"","delete"],[0,2,1,"","delete_async"],[0,2,1,"","get_all"],[0,2,1,"","get_all_async"],[0,2,1,"","get_one"],[0,2,1,"","get_one_async"],[0,2,1,"","update"],[0,2,1,"","update_async"]],"flashcards_core.database.exporter":[[0,3,1,"","DEFAULT_EXCLUDE_FIELDS"],[0,4,1,"","export_to_dict"],[0,4,1,"","export_to_json"],[0,4,1,"","hierarchy_to_json"]],"flashcards_core.database.importer":[[0,4,1,"","datetime_hook"],[0,4,1,"","import_from_dict"],[0,4,1,"","import_from_json"],[0,4,1,"","import_to_associative_table"],[0,4,1,"","import_to_table"]],"flashcards_core.database.models":[[2,0,0,"-","cards"],[2,0,0,"-","decks"],[2,0,0,"-","facts"],[2,0,0,"-","reviews"],[2,0,0,"-","tags"]],"flashcards_core.database.models.cards":[[2,1,1,"","Card"],[2,3,1,"","CardAnswerContext"],[2,3,1,"","CardQuestionContext"],[2,3,1,"","CardTag"],[2,3,1,"","RelatedCard"]],"flashcards_core.database.models.cards.Card":[[2,5,1,"","answer"],[2,5,1,"","answer_context_facts"],[2,5,1,"","answer_id"],[2,2,1,"","assign_answer_context"],[2,2,1,"","assign_answer_context_async"],[2,2,1,"","assign_question_context"],[2,2,1,"","assign_question_context_async"],[2,2,1,"","assign_tag"],[2,2,1,"","assign_tag_async"],[2,5,1,"","deck"],[2,5,1,"","deck_id"],[2,5,1,"","id"],[2,5,1,"","question"],[2,5,1,"","question_context_facts"],[2,5,1,"","question_id"],[2,5,1,"","related_cards"],[2,2,1,"","remove_answer_context"],[2,2,1,"","remove_answer_context_async"],[2,2,1,"","remove_question_context"],[2,2,1,"","remove_question_context_async"],[2,2,1,"","remove_tag"],[2,2,1,"","remove_tag_async"],[2,5,1,"","reviews"],[2,5,1,"","tags"]],"flashcards_core.database.models.decks":[[2,1,1,"","Deck"],[2,3,1,"","DeckTag"]],"flashcards_core.database.models.decks.Deck":[[2,5,1,"","algorithm"],[2,2,1,"","assign_tag"],[2,5,1,"","cards"],[2,5,1,"","description"],[2,2,1,"","get_by_name"],[2,2,1,"","get_by_name_async"],[2,5,1,"","id"],[2,5,1,"","name"],[2,5,1,"","parameters"],[2,2,1,"","remove_tag"],[2,2,1,"","remove_tag_async"],[2,5,1,"","state"],[2,5,1,"","tags"],[2,2,1,"","unseen_cards_list"],[2,2,1,"","unseen_cards_list_async"],[2,2,1,"","unseen_cards_number"],[2,2,1,"","unseen_cards_number_async"]],"flashcards_core.database.models.facts":[[2,1,1,"","Fact"],[2,3,1,"","RelatedFact"]],"flashcards_core.database.models.facts.Fact":[[2,2,1,"","assign_tag"],[2,2,1,"","assign_tag_async"],[2,5,1,"","format"],[2,5,1,"","id"],[2,5,1,"","related_facts"],[2,2,1,"","remove_tag"],[2,2,1,"","remove_tag_async"],[2,5,1,"","tags"],[2,5,1,"","value"]],"flashcards_core.database.models.reviews":[[2,1,1,"","Review"]],"flashcards_core.database.models.reviews.Review":[[2,5,1,"","algorithm"],[2,5,1,"","card"],[2,5,1,"","card_id"],[2,5,1,"","datetime"],[2,5,1,"","id"],[2,5,1,"","result"]],"flashcards_core.database.models.tags":[[2,1,1,"","Tag"]],"flashcards_core.database.models.tags.Tag":[[2,2,1,"","get_by_name"],[2,2,1,"","get_by_name_async"],[2,5,1,"","id"],[2,5,1,"","name"]],"flashcards_core.schedulers":[[3,0,0,"-","base"],[3,4,1,"","get_available_schedulers"],[3,4,1,"","get_scheduler_class"],[3,4,1,"","get_scheduler_for_deck"],[3,0,0,"-","random"]],"flashcards_core.schedulers.base":[[3,1,1,"","BaseScheduler"]],"flashcards_core.schedulers.base.BaseScheduler":[[3,5,1,"","deck"],[3,2,1,"","next_card"],[3,2,1,"","process_test_result"],[3,5,1,"","session"]],"flashcards_core.schedulers.random":[[3,3,1,"","LAST_REVIEWED_CARD"],[3,3,1,"","NEVER_REPEAT"],[3,1,1,"","RandomScheduler"],[3,3,1,"","UNSEEN_FIRST"]],"flashcards_core.schedulers.random.RandomScheduler":[[3,2,1,"","next_card"],[3,2,1,"","process_test_result"]],"flashcards_core.study":[[4,1,1,"","Study"]],"flashcards_core.study.Study":[[4,2,1,"","next"]],flashcards_core:[[0,0,0,"-","database"],[3,0,0,"-","schedulers"],[4,0,0,"-","study"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","data","Python data"],"4":["py","function","Python function"],"5":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:data","4":"py:function","5":"py:attribute"},terms:{"0":[0,1],"00":0,"01":0,"1":[0,1],"100":0,"12":0,"2":0,"2021":0,"abstract":3,"boolean":3,"break":2,"case":3,"class":4,"default":0,"do":[1,2,3],"function":[0,1],"import":1,"int":[0,2],"long":1,"new":[0,1,3],"return":[0,2,3,4],"short":[1,2],"true":[0,1,2,3],"try":1,"while":1,A:[0,1,2,3],For:[1,2],If:[0,1,3],In:[0,1,3],It:[0,1,2],Its:0,Or:1,The:[0,1,2,3],These:0,To:1,_hierarchi:0,abc:3,abov:[0,1],absolut:1,achiev:1,activ:1,actual:2,ad:0,add:[1,2],addit:[1,3],algorithm:[0,1,2,3,4],algorithm_nam:3,algorothm:2,all:[0,2,4],allow:2,alreadi:0,also:1,among:3,amount:1,an:[0,1,2,4],ani:[0,1,2,3,4],anki:1,answer:[0,1,2],answer_context_fact:2,answer_id:[0,1,2],anyth:1,api:1,appli:0,applic:[1,2],ar:[0,1,2],argument:0,around:0,articl:1,ask:1,assign:[2,3],assign_answer_context:2,assign_answer_context_async:2,assign_question_context:2,assign_question_context_async:2,assign_tag:2,assign_tag_async:2,associ:2,assum:1,async:[0,2],asyncio:[0,2],attribut:0,autogener:1,avail:[0,1],backward:1,base:[2,4],becaus:2,been:[0,2],belong:[2,3],below:1,benefit:1,between:[1,2],bin:1,bird:1,black:1,bool:0,built:0,bye:1,call:[0,1],can:[0,1,2,3],cano:4,card:[0,1,3,4],card_answer_context:2,card_id:[0,2],card_question_context:2,card_to_studi:1,cardanswercontext:2,cardquestioncontext:2,cards_studi:1,cardtag:2,categor:0,cd:1,chang:1,check:[0,1],check_same_thread:0,choos:3,chosen:3,classmethod:[0,2],cli:1,clone:1,colleagu:1,collect:1,column:[0,2],com:1,commit:1,compat:[1,2],complet:1,compon:1,con:1,configur:[2,3],connect:[0,1,2],connect_arg:0,constraint:3,contain:[0,2],content:2,context:[1,2],conveni:4,copi:2,core:0,correct:1,correspond:[0,2,3],creat:[0,1,3,4],create_async:0,create_engin:0,crud:2,crudoper:[0,2],current:2,curv:1,data:[0,2],databas:[1,3,4],database_path:0,date:[0,2],datetim:[0,2],datetime_hook:0,db:0,decid:[1,2],deck:[0,1,3,4],deck_id:[0,1,2],decktag:[0,2],decl_api:[0,2],decod:2,default_exclude_field:0,defin:0,definit:0,delet:0,delete_async:0,depend:[2,4],descript:[0,1,2],design:[1,2],detail:1,develop:1,dict:0,dictionari:0,differ:3,discov:0,discover:2,discoveri:0,doc:[0,1],document:0,doe:3,don:0,done:2,drop:2,dump:0,duolingo:1,easi:2,easili:0,ebisu:1,edit:1,element:0,els:1,empti:0,encod:0,engin:0,entiti:0,error:0,etc:[0,1,2],exampl:[0,1,2],except:[0,1,3],exclud:0,exclude_field:0,exclus:0,exist:[0,1,2],expect:0,experi:1,explan:1,export_to_dict:0,export_to_json:0,extra:1,f:1,fact:[0,1],fact_id:2,facttag_id:2,fail:1,fairli:1,fals:[0,2],favour:2,featur:1,field:[0,2,3],file:2,find:[0,1],first:1,flag:1,flake8:1,flashcard:0,flashcards_cor:[0,1,2,3,4],follow:[0,1],foreign:1,foreignkei:2,forget:1,forgotten:1,format:[0,1,2],found:0,freezegun:2,friendli:[0,2],from:[0,1,2,3],frontend:[1,2,3],func:2,further:3,gener:[0,3],get:1,get_al:0,get_all_async:0,get_available_schedul:3,get_by_nam:2,get_by_name_async:2,get_on:0,get_one_async:0,get_scheduler_class:3,get_scheduler_for_deck:3,git:1,github:1,give:[0,2,3],given:[0,2,3],good:2,googl:1,great:1,greatest:1,guid:2,ha:3,have:[0,1,2],help:[1,2],here:[0,1,3],hierarchi:0,hierarchy_to_json:0,hint:2,hit:1,hold:2,home:0,hook:1,how:[1,2],html:2,http:1,i:2,id:[0,1,2,3],imag:[1,2],impact:1,implement:3,import_from_dict:0,import_from_json:0,import_to_associative_t:0,import_to_t:0,includ:[0,1],index:0,info:0,init_db:[0,1,2,3],init_sess:0,initi:[0,1,4],input:[0,1],instead:0,instruct:0,integr:0,interact:3,interfac:1,intern:0,interpret:2,issu:2,item:1,its:0,json:[0,2],json_dict:0,json_kwarg:0,json_str:0,just:[1,2,4],keep:3,kei:[0,1,2],keyboardinterrupt:1,know:1,known:3,kwarg:[0,2],lambda:2,languag:1,larg:1,last:[1,3],last_reviewed_card:[0,3],later:3,learn:1,least:1,lenght:1,like:[0,1,2],limit:0,link:1,list:[0,1,2,3],load:0,look:[0,1],lot:2,m:1,made:[0,1],mai:0,main:1,make:[0,1,3],mandatori:3,mani:[1,2],map:0,markdown:2,match:[0,2],maximum:0,mean:2,memor:1,metadata:2,method:[0,3],might:[1,2,3],minor:1,mix:0,mixtur:0,model:[0,1,3,4],modifi:0,more:[0,1,3,4],most:1,must:0,my:1,n:1,name:[0,1,2,3],need:0,never:[2,3],never_repeat:3,next:[1,3,4],next_card:3,none:[0,2,3,4],normal:0,note:[0,1,2],notic:1,now:2,nstudi:1,nullabl:2,number:[0,2],obj:0,object:[0,1,2,4],object_id:0,objectnotfoundexcept:0,objects_to_export:0,observ:2,offset:0,onc:4,one:[0,2,3],ones:[0,1,3],onli:[0,1],opposit:1,optim:1,option:[0,2,4],order:1,original_card_id:2,original_fact_id:2,orm:[0,2,3,4],other:[0,1],out:1,output:0,over:1,overal:0,overridden:0,own:1,packag:1,pagin:0,pair:1,paramet:[0,2,3,4],pass:0,path:2,perform:[0,2],pick:3,pip:1,plaintext:2,pointer:3,popular:1,possibl:1,postgr:0,potenti:0,power:1,pr:1,practic:3,pre:1,primari:2,primary_kei:2,print:1,prioriti:3,pro:1,probabl:3,process:[3,4],process_test_result:3,propos:1,protocol:0,provid:[0,1,4],pypi:1,pytest:1,python3:1,python:1,queri:0,question:[0,1,2],question_context_fact:2,question_id:[0,1,2],radic:1,rais:[0,3],random:[0,1],rate:1,rather:1,re:[0,1,3],readi:3,realli:0,reconstruct:0,recurs:0,refer:0,refresh:2,relat:[0,2],related_card:2,related_card_id:2,related_fact:2,related_fact_id:2,relatedcard:2,relatedfact:2,relationship:[0,2],rememb:[0,1],remov:2,remove_answer_context:2,remove_answer_context_async:2,remove_question_context:2,remove_question_context_async:2,remove_tag:2,remove_tag_async:2,renam:2,repationship:2,repl:1,repo:1,repres:2,represent:0,request:3,requir:0,respect:3,result:[0,2,3,4],review:[0,1,3,4],row:3,run:1,runner:0,s:[0,1,2],same:[0,3],save:4,schedul:[1,2,4],schema:[0,2],scholar:1,scienc:1,scientif:1,script:1,section:1,see:[0,1,2,3],seen:[1,2],send:[1,3],serial:0,serializ:0,seriou:2,session:[0,1,2,3,4],sessionmak:[0,1],set:0,setup:1,sever:[0,2],should:[0,1,2,4],show:3,simpl:[0,1],simpler:1,singl:1,skip:0,sm2:1,so:[0,1,2,3],some:[0,1,2],somehow:2,song:1,soon:1,sound:1,sourc:1,specifi:0,sql:0,sqlalchemi:[0,2,3,4],sqlite:0,sqlite_dev:0,sr:2,standard:[0,1],start:[0,1,4],state:[0,2],stateless:4,statist:3,still:1,stop:0,stop_on_error:0,store:[2,3],str:[0,2,3],string:[0,2],structur:0,studi:[1,3],studied_card:4,subclass:[0,3],subset:0,summari:1,supermemo:1,support:1,sure:[0,3],t:0,tabl:[0,2],tablenam:0,tag:[0,1],tag_id:2,taken:0,term:1,test:[0,1,2,3,4],text:[0,1],than:[3,4],thank:1,thei:[0,1,2],them:[0,1,4],therefor:3,thi:[0,1,2,3,4],those:2,through:[0,1],time:[1,2],track:3,trivia:1,trivial:1,truth:1,twice:3,two:1,type:[0,2,3,4],understand:[0,1,2],understando:2,unlik:2,unseen:3,unseen_cards_list:2,unseen_cards_list_async:2,unseen_cards_numb:2,unseen_cards_number_async:2,unseen_first:[0,3],until:1,up:2,updat:0,update_async:0,url:[0,2],us:[0,1,2,3],usag:0,uuid:[0,2],valid:[0,2],valu:[0,1,2,3],valueerror:3,venv:1,veri:1,vocabulari:1,wa:[0,1,2,3],wai:1,we:[1,3],web:1,welcom:1,well:0,were:0,what:[0,1,2],whatsoev:1,where:0,which:[0,1,2],wikipedia:1,wish:[0,2],without:2,won:0,work:0,world:1,would:0,wrapper:0,write:1,wrong:1,yaml:0,yet:1,you:[0,1,2],your:1},titles:["Database","Flashcards Core","Database Model Classes","Schedulers","Study API"],titleterms:{"class":[0,2,3],"export":0,"import":0,api:4,base:[0,3],baseschedul:3,card:2,contact:1,contribut:1,contributor:1,core:1,crud:0,databas:[0,2],deck:2,document:1,fact:2,flashcard:1,helper:[0,3],instal:1,introduct:1,librari:1,model:2,order:3,random:3,randomschedul:3,refer:1,repetit:1,review:2,schedul:3,softwar:1,space:1,sr:1,structur:1,studi:4,tag:2,usag:1,util:0,version:1}})