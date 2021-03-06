# Configuration

You can either configure Lithops with configuration file or provide configuration keys in runtime
## Create a configuration file

To configure Lithops through a [configuration template file](config_template.yaml) you have multiple options:

1. Create e new file called `config` in the `~/.lithops` folder.

2. Create a new file called `.lithops_config` in the root directory of your project from where you will execute your Lithops scripts.

3. Create the config file in any other location and configure the `LITHOPS_CONFIG_FILE` system environment variable:


	 	LITHOPS_CONFIG_FILE=<CONFIG_FILE_LOCATION>

```python
import lithops

def hello_world(name):
    return 'Hello {}!'.format(name)

if __name__ == '__main__':
    fexec = lithops.function_executor()
    fexec.call_async(hello, 'World')
    print(fexec.get_result())
```

    
## Configuration in runtime

An alternative mode of configuration is to use a python dictionary. This option allows to pass all the configuration details as part of the Lithops invocation in runtime, for example:

```python
import lithops

config = {'lithops' : {'storage_bucket' : 'BUCKET_NAME'},

          'ibm_cf':  {'endpoint': 'HOST',
                      'namespace': 'NAMESPACE',
                      'api_key': 'API_KEY'},

          'ibm_cos': {'endpoint': 'ENDPOINT',
                      'private_endpoint': 'PRIVATE_ENDPOINT',
                      'api_key': 'API_KEY'}}

def hello_world(name):
    return 'Hello {}!'.format(name)

if __name__ == '__main__':
    fexec = lithops.function_executor(config=config)
    fexec.call_async(hello, 'World')
    print(fexec.get_result())
```

## Configure your Compute and Storage backends

<table>
<tr>
<th align="center">
<img width="441" height="1px">
<p> 
<small>
Serverless Compute Backends
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
Storage Backends
</small>
</p>
</th>
</tr>
<tr>
<td>

- [IBM Cloud Functions](compute/ibm_cf.md)
- [IBM Code Engine](compute/code_engine.md)
- [Knative](compute/knative.md)
- [OpenWhisk](compute/openwhisk.md)
- [Docker](compute/docker.md)
- [Loclahost](compute/localhost.md)
- [AWS Lambda](compute/aws_lambda.md)
- [Google Cloud Functions](compute/gcp_functions.md)
- [Azure Functions](compute/azure_fa.md)
- [Aliyun functions](compute/aliyun_fc.md)
  
</td>
<td>
  
- [IBM Cloud Object Storage](storage/ibm_cos.md)
- [Infinispan](storage/infinispan.md)
- [Ceph](storage/ceph.md)
- [Redis](storage/redis.md)
- [OpenStack Swift](storage/swift.md)
- [Localhost](storage/localhost.md)
- [AWS S3](storage/aws_s3.md)
- [Google Cloud Storage](storage/gcp_storage.md)
- [Azure Blob Storage](storage/azure_blob.md)
- [Aliyun Object Storage Service](storage/aliyun_oss.md)
  
</td>
</tr>
</table>

## Verify

Test if Lithops is working properly:

```python
import lithops
   
def hello_world(name):
    return 'Hello {}!'.format(name)
    
if __name__ == '__main__':
    fexec = lithops.function_executor()
    exec.call_async(hello_world, 'World')
    print("Response from function: ", fexec.get_result())
   ```

## Configure multiple backends

Lithops configuration allows to provide the access credentials to multiple compute and storage backends. by default it will choose those backends set in the  *compute_backend* and *storage_backend* parameters in the lithops section. To switch between backends you simply need to change the *compute_backend* and *storage_backend* parameters and point to the backends you pretend to use:
    
```yaml
lithops:
   compute_backend: localhost
   storage_backend: ibm_cos
```
    
Alternatively, regardless of what you set in the configuration file, you can chose your desired compute and storage backends in runtime, when you create an executor. These parameters will overwrite the configuration, for example:

```python
fexec = lithops.function_executor(compute_backend='ibm_cf', storage_backned='ibm_cos')
...
fexec = lithops.function_executor(compute_backend='knative', storage_bakcned='ceph')
...
```


## Using RabbitMQ to monitor function activations (optional)

By default, Lithops uses the storage backend to monitor function activations: Each function activation stores a file named *{id}/status.json* to the Object Storage when it finishes its execution. This file contains some statistics about the execution, including if the function activation ran successfully or not. Having these files, the default monitoring approach is based on polling the Object Store each X seconds to know which function activations have finished and which not.

As this default approach can slow-down the total application execution time, due to the number of requests it has to make against the object store, in Lithops we integrated a RabitMQ service to monitor function activations in real-time. With RabitMQ, the content of the *{id}/status.json* file is sent trough a queue. This speeds-up total application execution time, since Lithops only needs one connection to the messaging service to monitor all function activations. We currently support the AMQP protocol. To enable Lithops to use this service, add the *AMQP_URL* key into the *rabbitmq* section in the configuration, for example:

```yaml
rabbitmq:
    amqp_url: <AMQP_URL>  # amqp://
```

In addition, activate the monitoring service by setting *rabbitmq_monitor : True* in the configuration (Lithops section):

```yaml
lithops:
   rabbitmq_monitor: True
```

or in the executor by:

```python
fexec = lithops.function_executor(rabbitmq_monitor=True)
```


## Summary of configuration keys for Lithops

|Group|Key|Default|Mandatory|Additional info|
|---|---|---|---|---|
|lithops|storage_bucket | |yes | Any bucket that exists in your COS account. This will be used by Lithops for intermediate data |
|lithops|data_cleaner |True|no|If set to True, then cleaner will automatically delete temporary data that was written into `storage_bucket/lithops.jobs`|
|lithops | storage_backend | ibm_cos | no | Storage backend implementation. IBM Cloud Object Storage is the default |
|lithops | compute_backend | ibm_cf | no | Compute backend implementation. IBM Cloud Functions is the default |
|lithops | rabbitmq_monitor | False | no | Activate the rabbitmq monitoring feature |
|lithops | workers | Depends of the ComputeBackend | no | Max number of concurrent workers |
|lithops| runtime_timeout | 600 |no |  Default runtime timeout (in seconds) |
|lithops| runtime_memory | 256 | no | Default runtime memory (in MB) |
|lithops| data_limit | 4 | no | Max (iter)data size (in MB). Set to False for unlimited size |
