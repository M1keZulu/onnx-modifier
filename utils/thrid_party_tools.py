import os
import copy
import onnx
try:
    import onnx_tool
except ModuleNotFoundError:
    os.system("pip install onnx-tool==0.6.4")
    import onnx_tool

def shape_inference_using_onnx_tool(model_proto):
    g = onnx_tool.Graph(model_proto.graph, verbose=False)
    g.shape_infer()
    
    inferred_value_info = []
    for key in g.dynamics:
        tensor = g.tensormap[key]
        vinfo = tensor.make_value_proto()
        if vinfo is None:
            continue
        if vinfo not in inferred_value_info:
            inferred_value_info.append(vinfo)

    return inferred_value_info

def shape_inference_primitive(model_proto):
    shape_info = onnx.shape_inference.infer_shapes(model_proto)
    inferred_value_info = [v for v in shape_info.graph.value_info]
    
    return inferred_value_info

def get_infered_shape(model_proto):
    inferred_value_info = None
    print("[EXPERIMENTAL] Do shape inference automatically...")
    reset_model_proto = copy.deepcopy(model_proto)
    del reset_model_proto.graph.value_info[:]
    del reset_model_proto.graph.output[:]
    # try:
    #     inferred_value_info = shape_inference_using_onnx_tool(reset_model_proto)
    # except:
    print("shape inference using onnx-tool fails, fallback to primitive ONNX Python API.")
    inferred_value_info = shape_inference_primitive(reset_model_proto)
    
    return inferred_value_info