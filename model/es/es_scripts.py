from model.es.base_model import get_es_client

engine_sort_default_bk = """
    double total_point=0;
    for(def sort_param:params.sort_params){
        double point=0;
        if (sort_param.type.equals("list")){
            for(def key:doc[sort_param.key]){
                def sub_key=String.valueOf(key);
                point += sort_params.params.containsKey(sub_key) ? sort_param.get(sub_key):0
            }
        }
        total_point += sort_param.weight * point
    }
    return total_point;
    """

engine_sort_default = """
                      double total_point=0;
                      for(def sort_param:params.sort_params){
                        double point=0;
                        if(sort_param.type.equals("max") && doc[sort_param.key].length>0){
                          def key=Long.toString(Collections.max(doc[sort_param.key]));
                          point += sort_param.params.containsKey(key) ? sort_param.params.get(key):0;
                        }else if(sort_param.type.equals("min") && doc[sort_param.key].length>0){
                          def key=Long.toString(Collections.min(doc[sort_param.key]));
                          point += sort_param.params.containsKey(key) ? sort_param.params.get(key):0;
                        }else if(sort_param.type.equals("key")){
                          def key=String.valueOf(doc[sort_param.key]);
                          point += sort_param.params.containsKey(key) ? sort_param.params.get(key):0;
                        }else if(sort_param.type.equals("list")){
                          for(def key:doc[sort_param.key]){
                            def sub_key=String.valueOf(key);
                            point += sort_param.params.containsKey(sub_key) ? sort_param.params.get(sub_key):0;
                          }
                        }
                        total_point += sort_param.weight * point;
                      }

                      return total_point;
                    """

script_map = {
    'engine_sort_default': engine_sort_default
}

def put_script(script_name):
    if script_name not in script_map:
        print("script: ({}) not found".format(script_name))
    script_body = {
        "script": {
            "lang": "painless",
            "source": script_map[script_name]
        }
    }
    es = get_es_client()
    es.put_script(id=script_name, body=script_body)

def put_scripts():
    for script_name in script_map.keys():
        put_script(script_name)