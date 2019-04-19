import paddle.fluid as fluid
import paddlehub as hub

module = hub.Module(name="ernie")
inputs, outputs, program = module.context(trainable=True)
reader = hub.reader.ClassifyReader(hub.dataset.ChnSentiCorp(),
                                   module.get_vocab_path())
task = hub.create_text_cls_task(feature=outputs["pooled_output"], num_classes=2)
strategy = hub.AdamWeightDecayStrategy(learning_rate=5e-5)
config = hub.RunConfig(use_cuda=True, num_epoch=3, strategy=strategy)
feed_list = [
    inputs["input_ids"].name, inputs["position_ids"].name,
    inputs["segment_ids"].name, inputs["input_mask"].name,
    task.variable("label").name
]
hub.finetune_and_eval(task, reader, feed_list, config)
