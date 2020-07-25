from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import LabelSelector, ListMeta, ObjectMeta
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.yaml.yaml_handling import HelmYaml


class ScopedResourceSelectorRequirement(HelmYaml):
    """
    :param operator:Represents a scope's relationship to a set of values. Valid \
        operators are In, NotIn, Exists, DoesNotExist.
    :type operator: str
    :param scope_name:The name of the scope that the selector applies to.
    :type scope_name: str
    :param values:An array of string values. If the operator is In or NotIn, the \
        values array must be non-empty. If the operator is Exists or DoesNotExist, the \
        values array must be empty. This array is replaced during a strategic merge \
        patch.
    :type values: List[str]
    """

    def __init__(self, operator: str, scope_name: str, values: List[str]):
        self.operator = operator
        self.scopeName = scope_name
        self.values = values


class ScopeSelector(HelmYaml):
    """
    :param match_expressions:A list of scope selector requirements by scope of the \
        resources.
    :type match_expressions: Optional[List[ScopedResourceSelectorRequirement]]
    """

    def __init__(
        self,
        match_expressions: Optional[List[ScopedResourceSelectorRequirement]] = None,
    ):
        self.matchExpressions = match_expressions


class ObjectFieldSelector(HelmYaml):
    """
    :param field_path:Path of the field to select in the specified API version.
    :type field_path: str
    :param api_version:Version of the schema the FieldPath is written in terms of, \
        defaults to "v1".
    :type api_version: Optional[str]
    """

    def __init__(self, field_path: str, api_version: Optional[str] = None):
        self.fieldPath = field_path
        self.apiVersion = api_version


class ResourceFieldSelector(HelmYaml):
    """
    :param container_name:Container name: required for volumes, optional for env vars
    :type container_name: str
    :param resource:Required: resource to select
    :type resource: str
    :param divisor:Specifies the output format of the exposed resources, defaults to \
        "1"
    :type divisor: Optional[str]
    """

    def __init__(
        self, container_name: str, resource: str, divisor: Optional[str] = None
    ):
        self.containerName = container_name
        self.resource = resource
        self.divisor = divisor


class DownwardAPIVolumeFile(HelmYaml):
    """
    :param field_ref:Required: Selects a field of the pod: only annotations, labels, \
        name and namespace are supported.
    :type field_ref: ObjectFieldSelector
    :param path:Required: Path is  the relative path name of the file to be created. \
        Must not be absolute or contain the '..' path. Must be utf-8 encoded. The \
        first item of the relative path must not start with '..'
    :type path: str
    :param resource_field_ref:Selects a resource of the container: only resources \
        limits and requests (limits.cpu, limits.memory, requests.cpu and \
        requests.memory) are currently supported.
    :type resource_field_ref: ResourceFieldSelector
    :param mode:Optional: mode bits to use on this file, must be a value between 0 and \
        0777. If not specified, the volume defaultMode will be used. This might be in \
        conflict with other options that affect the file mode, like fsGroup, and the \
        result can be other mode bits set.
    :type mode: Optional[int]
    """

    def __init__(
        self,
        field_ref: ObjectFieldSelector,
        path: str,
        resource_field_ref: ResourceFieldSelector,
        mode: Optional[int] = None,
    ):
        self.fieldRef = field_ref
        self.path = path
        self.resourceFieldRef = resource_field_ref
        self.mode = mode


class DownwardAPIProjection(HelmYaml):
    """
    :param items:Items is a list of DownwardAPIVolume file
    :type items: List[DownwardAPIVolumeFile]
    """

    def __init__(self, items: List[DownwardAPIVolumeFile]):
        self.items = items


class LimitRangeItem(HelmYaml):
    """
    :param default:Default resource requirement limit value by resource name if \
        resource limit is omitted.
    :type default: dict
    :param default_request:DefaultRequest is the default resource requirement request \
        value by resource name if resource request is omitted.
    :type default_request: dict
    :param max:Max usage constraints on this kind by resource name.
    :type max: dict
    :param min:Min usage constraints on this kind by resource name.
    :type min: dict
    :param type:Type of resource that this limit applies to.
    :type type: str
    :param max_limit_request_ratio:MaxLimitRequestRatio if specified, the named \
        resource must have a request and limit that are both non-zero where limit \
        divided by request is less than or equal to the enumerated value; this \
        represents the max burst for the named resource.
    :type max_limit_request_ratio: Optional[dict]
    """

    def __init__(
        self,
        default: dict,
        default_request: dict,
        max: dict,
        min: dict,
        type: str,
        max_limit_request_ratio: Optional[dict] = None,
    ):
        self.default = default
        self.defaultRequest = default_request
        self.max = max
        self.min = min
        self.type = type
        self.maxLimitRequestRatio = max_limit_request_ratio


class ClientIPConfig(HelmYaml):
    """
    :param timeout_seconds:timeoutSeconds specifies the seconds of ClientIP type \
        session sticky time. The value must be >0 && <=86400(for 1 day) if \
        ServiceAffinity == "ClientIP". Default value is 10800(for 3 hours).
    :type timeout_seconds: int
    """

    def __init__(self, timeout_seconds: int):
        self.timeoutSeconds = timeout_seconds


class SessionAffinityConfig(HelmYaml):
    """
    :param client_ip:clientIP contains the configurations of Client IP based session \
        affinity.
    :type client_ip: ClientIPConfig
    """

    def __init__(self, client_ip: ClientIPConfig):
        self.clientIP = client_ip


class ResourceQuotaSpec(HelmYaml):
    """
    :param hard:hard is the set of desired hard limits for each named resource. More \
        info: https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :type hard: dict
    :param scope_selector:scopeSelector is also a collection of filters like scopes \
        that must match each object tracked by a quota but expressed using \
        ScopeSelectorOperator in combination with possible values. For a resource to \
        match, both scopes AND scopeSelector (if specified in spec), must be matched.
    :type scope_selector: Optional[ScopeSelector]
    :param scopes:A collection of filters that must match each object tracked by a \
        quota. If not specified, the quota matches all objects.
    :type scopes: Optional[List[str]]
    """

    def __init__(
        self,
        hard: dict,
        scope_selector: Optional[ScopeSelector] = None,
        scopes: Optional[List[str]] = None,
    ):
        self.hard = hard
        self.scopeSelector = scope_selector
        self.scopes = scopes


class ResourceQuota(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the desired quota. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ResourceQuotaSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: ResourceQuotaSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class KeyToPath(HelmYaml):
    """
    :param key:The key to project.
    :type key: str
    :param path:The relative path of the file to map the key to. May not be an \
        absolute path. May not contain the path element '..'. May not start with the \
        string '..'.
    :type path: str
    :param mode:Optional: mode bits to use on this file, must be a value between 0 and \
        0777. If not specified, the volume defaultMode will be used. This might be in \
        conflict with other options that affect the file mode, like fsGroup, and the \
        result can be other mode bits set.
    :type mode: Optional[int]
    """

    def __init__(self, key: str, path: str, mode: Optional[int] = None):
        self.key = key
        self.path = path
        self.mode = mode


class SecretProjection(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param optional:Specify whether the Secret or its key must be defined
    :type optional: bool
    :param items:If unspecified, each key-value pair in the Data field of the \
        referenced Secret will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the Secret, the volume setup will \
        error unless it is marked optional. Paths must be relative and may not contain \
        the '..' path or start with '..'.
    :type items: Optional[List[KeyToPath]]
    """

    def __init__(
        self, name: str, optional: bool, items: Optional[List[KeyToPath]] = None
    ):
        self.name = name
        self.optional = optional
        self.items = items


class ExecAction(HelmYaml):
    """
    :param command:Command is the command line to execute inside the container, the \
        working directory for the command  is root ('/') in the container's \
        filesystem. The command is simply exec'd, it is not run inside a shell, so \
        traditional shell instructions ('|', etc) won't work. To use a shell, you need \
        to explicitly call out to that shell. Exit status of 0 is treated as \
        live/healthy and non-zero is unhealthy.
    :type command: List[str]
    """

    def __init__(self, command: List[str]):
        self.command = command


class VolumeDevice(HelmYaml):
    """
    :param name:name must match the name of a persistentVolumeClaim in the pod
    :type name: str
    :param device_path:devicePath is the path inside of the container that the device \
        will be mapped to.
    :type device_path: str
    """

    def __init__(self, name: str, device_path: str):
        self.name = name
        self.devicePath = device_path


class ConfigMapKeySelector(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param key:The key to select.
    :type key: str
    :param optional:Specify whether the ConfigMap or its key must be defined
    :type optional: bool
    """

    def __init__(self, name: str, key: str, optional: bool):
        self.name = name
        self.key = key
        self.optional = optional


class SecretKeySelector(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param key:The key of the secret to select from.  Must be a valid secret key.
    :type key: str
    :param optional:Specify whether the Secret or its key must be defined
    :type optional: bool
    """

    def __init__(self, name: str, key: str, optional: bool):
        self.name = name
        self.key = key
        self.optional = optional


class EnvVarSource(HelmYaml):
    """
    :param config_map_key_ref:Selects a key of a ConfigMap.
    :type config_map_key_ref: ConfigMapKeySelector
    :param field_ref:Selects a field of the pod: supports metadata.name, \
        metadata.namespace, metadata.labels, metadata.annotations, spec.nodeName, \
        spec.serviceAccountName, status.hostIP, status.podIP, status.podIPs.
    :type field_ref: ObjectFieldSelector
    :param resource_field_ref:Selects a resource of the container: only resources \
        limits and requests (limits.cpu, limits.memory, limits.ephemeral-storage, \
        requests.cpu, requests.memory and requests.ephemeral-storage) are currently \
        supported.
    :type resource_field_ref: ResourceFieldSelector
    :param secret_key_ref:Selects a key of a secret in the pod's namespace
    :type secret_key_ref: SecretKeySelector
    """

    def __init__(
        self,
        config_map_key_ref: ConfigMapKeySelector,
        field_ref: ObjectFieldSelector,
        resource_field_ref: ResourceFieldSelector,
        secret_key_ref: SecretKeySelector,
    ):
        self.configMapKeyRef = config_map_key_ref
        self.fieldRef = field_ref
        self.resourceFieldRef = resource_field_ref
        self.secretKeyRef = secret_key_ref


class EnvVar(HelmYaml):
    """
    :param name:Name of the environment variable. Must be a C_IDENTIFIER.
    :type name: str
    :param value:Variable references $(VAR_NAME) are expanded using the previous \
        defined environment variables in the container and any service environment \
        variables. If a variable cannot be resolved, the reference in the input string \
        will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: \
        $$(VAR_NAME). Escaped references will never be expanded, regardless of whether \
        the variable exists or not. Defaults to "".
    :type value: Optional[str]
    :param value_from:Source for the environment variable's value. Cannot be used if \
        value is not empty.
    :type value_from: Optional[EnvVarSource]
    """

    def __init__(
        self,
        name: str,
        value: Optional[str] = None,
        value_from: Optional[EnvVarSource] = None,
    ):
        self.name = name
        self.value = value
        self.valueFrom = value_from


class ResourceRequirements(HelmYaml):
    """
    :param limits:Limits describes the maximum amount of compute resources allowed. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type limits: Optional[dict]
    :param requests:Requests describes the minimum amount of compute resources \
        required. If Requests is omitted for a container, it defaults to Limits if \
        that is explicitly specified, otherwise to an implementation-defined value. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type requests: Optional[dict]
    """

    def __init__(self, limits: Optional[dict] = None, requests: Optional[dict] = None):
        self.limits = limits
        self.requests = requests


class SELinuxOptions(HelmYaml):
    """
    :param level:Level is SELinux level label that applies to the container.
    :type level: str
    :param role:Role is a SELinux role label that applies to the container.
    :type role: str
    :param type:Type is a SELinux type label that applies to the container.
    :type type: str
    :param user:User is a SELinux user label that applies to the container.
    :type user: str
    """

    def __init__(self, level: str, role: str, type: str, user: str):
        self.level = level
        self.role = role
        self.type = type
        self.user = user


class WindowsSecurityContextOptions(HelmYaml):
    """
    :param gmsa_credential_spec:GMSACredentialSpec is where the GMSA admission webhook \
        (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents of the \
        GMSA credential spec named by the GMSACredentialSpecName field.
    :type gmsa_credential_spec: str
    :param gmsa_credential_spec_name:GMSACredentialSpecName is the name of the GMSA \
        credential spec to use.
    :type gmsa_credential_spec_name: str
    :param run_as_user_name:The UserName in Windows to run the entrypoint of the \
        container process. Defaults to the user specified in image metadata if \
        unspecified. May also be set in PodSecurityContext. If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence.
    :type run_as_user_name: Optional[str]
    """

    def __init__(
        self,
        gmsa_credential_spec: str,
        gmsa_credential_spec_name: str,
        run_as_user_name: Optional[str] = None,
    ):
        self.gmsaCredentialSpec = gmsa_credential_spec
        self.gmsaCredentialSpecName = gmsa_credential_spec_name
        self.runAsUserName = run_as_user_name


class Capabilities(HelmYaml):
    """
    :param add:Added capabilities
    :type add: List[str]
    :param drop:Removed capabilities
    :type drop: List[str]
    """

    def __init__(self, add: List[str], drop: List[str]):
        self.add = add
        self.drop = drop


class SecurityContext(HelmYaml):
    """
    :param allow_privilege_escalation:AllowPrivilegeEscalation controls whether a \
        process can gain more privileges than its parent process. This bool directly \
        controls if the no_new_privs flag will be set on the container process. \
        AllowPrivilegeEscalation is true always when the container is: 1) run as \
        Privileged 2) has CAP_SYS_ADMIN
    :type allow_privilege_escalation: bool
    :param run_as_group:The GID to run the entrypoint of the container process. Uses \
        runtime default if unset. May also be set in PodSecurityContext.  If set in \
        both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :type run_as_group: int
    :param run_as_non_root:Indicates that the container must run as a non-root user. \
        If true, the Kubelet will validate the image at runtime to ensure that it does \
        not run as UID 0 (root) and fail to start the container if it does. If unset \
        or false, no such validation will be performed. May also be set in \
        PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence.
    :type run_as_non_root: bool
    :param se_linux_options:The SELinux context to be applied to the container. If \
        unspecified, the container runtime will allocate a random SELinux context for \
        each container.  May also be set in PodSecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence.
    :type se_linux_options: SELinuxOptions
    :param windows_options:The Windows specific settings applied to all containers. If \
        unspecified, the options from the PodSecurityContext will be used. If set in \
        both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :type windows_options: WindowsSecurityContextOptions
    :param capabilities:The capabilities to add/drop when running containers. Defaults \
        to the default set of capabilities granted by the container runtime.
    :type capabilities: Optional[Capabilities]
    :param privileged:Run container in privileged mode. Processes in privileged \
        containers are essentially equivalent to root on the host. Defaults to false.
    :type privileged: Optional[bool]
    :param proc_mount:procMount denotes the type of proc mount to use for the \
        containers. The default is DefaultProcMount which uses the container runtime \
        defaults for readonly paths and masked paths. This requires the ProcMountType \
        feature flag to be enabled.
    :type proc_mount: Optional[str]
    :param read_only_root_filesystem:Whether this container has a read-only root \
        filesystem. Default is false.
    :type read_only_root_filesystem: Optional[bool]
    :param run_as_user:The UID to run the entrypoint of the container process. \
        Defaults to user specified in image metadata if unspecified. May also be set \
        in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence.
    :type run_as_user: Optional[int]
    """

    def __init__(
        self,
        allow_privilege_escalation: bool,
        run_as_group: int,
        run_as_non_root: bool,
        se_linux_options: SELinuxOptions,
        windows_options: WindowsSecurityContextOptions,
        capabilities: Optional[Capabilities] = None,
        privileged: Optional[bool] = None,
        proc_mount: Optional[str] = None,
        read_only_root_filesystem: Optional[bool] = None,
        run_as_user: Optional[int] = None,
    ):
        self.allowPrivilegeEscalation = allow_privilege_escalation
        self.runAsGroup = run_as_group
        self.runAsNonRoot = run_as_non_root
        self.seLinuxOptions = se_linux_options
        self.windowsOptions = windows_options
        self.capabilities = capabilities
        self.privileged = privileged
        self.procMount = proc_mount
        self.readOnlyRootFilesystem = read_only_root_filesystem
        self.runAsUser = run_as_user


class SecretEnvSource(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param optional:Specify whether the Secret must be defined
    :type optional: bool
    """

    def __init__(self, name: str, optional: bool):
        self.name = name
        self.optional = optional


class ConfigMapEnvSource(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param optional:Specify whether the ConfigMap must be defined
    :type optional: bool
    """

    def __init__(self, name: str, optional: bool):
        self.name = name
        self.optional = optional


class EnvFromSource(HelmYaml):
    """
    :param config_map_ref:The ConfigMap to select from
    :type config_map_ref: ConfigMapEnvSource
    :param prefix:An optional identifier to prepend to each key in the ConfigMap. Must \
        be a C_IDENTIFIER.
    :type prefix: str
    :param secret_ref:The Secret to select from
    :type secret_ref: SecretEnvSource
    """

    def __init__(
        self,
        config_map_ref: ConfigMapEnvSource,
        prefix: str,
        secret_ref: SecretEnvSource,
    ):
        self.configMapRef = config_map_ref
        self.prefix = prefix
        self.secretRef = secret_ref


class TCPSocketAction(HelmYaml):
    """
    :param port:Number or name of the port to access on the container. Number must be \
        in the range 1 to 65535. Name must be an IANA_SVC_NAME.
    :type port: int
    :param host:Optional: Host name to connect to, defaults to the pod IP.
    :type host: Optional[str]
    """

    def __init__(self, port: int, host: Optional[str] = None):
        self.port = port
        self.host = host


class HTTPHeader(HelmYaml):
    """
    :param name:The header field name
    :type name: str
    :param value:The header field value
    :type value: str
    """

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class HTTPGetAction(HelmYaml):
    """
    :param http_headers:Custom headers to set in the request. HTTP allows repeated \
        headers.
    :type http_headers: List[HTTPHeader]
    :param path:Path to access on the HTTP server.
    :type path: str
    :param port:Name or number of the port to access on the container. Number must be \
        in the range 1 to 65535. Name must be an IANA_SVC_NAME.
    :type port: int
    :param host:Host name to connect to, defaults to the pod IP. You probably want to \
        set "Host" in httpHeaders instead.
    :type host: Optional[str]
    :param scheme:Scheme to use for connecting to the host. Defaults to HTTP.
    :type scheme: Optional[str]
    """

    def __init__(
        self,
        http_headers: List[HTTPHeader],
        path: str,
        port: int,
        host: Optional[str] = None,
        scheme: Optional[str] = None,
    ):
        self.httpHeaders = http_headers
        self.path = path
        self.port = port
        self.host = host
        self.scheme = scheme


class Handler(HelmYaml):
    """
    :param exec:One and only one of the following should be specified. Exec specifies \
        the action to take.
    :type exec: ExecAction
    :param http_get:HTTPGet specifies the http request to perform.
    :type http_get: HTTPGetAction
    :param tcp_socket:TCPSocket specifies an action involving a TCP port. TCP hooks \
        not yet supported
    :type tcp_socket: TCPSocketAction
    """

    def __init__(
        self, exec: ExecAction, http_get: HTTPGetAction, tcp_socket: TCPSocketAction
    ):
        self.exec = exec
        self.httpGet = http_get
        self.tcpSocket = tcp_socket


class Lifecycle(HelmYaml):
    """
    :param post_start:PostStart is called immediately after a container is created. If \
        the handler fails, the container is terminated and restarted according to its \
        restart policy. Other management of the container blocks until the hook \
        completes. More info: \
        https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks  # noqa
    :type post_start: Handler
    :param pre_stop:PreStop is called immediately before a container is terminated due \
        to an API request or management event such as liveness/startup probe failure, \
        preemption, resource contention, etc. The handler is not called if the \
        container crashes or exits. The reason for termination is passed to the \
        handler. The Pod's termination grace period countdown begins before the \
        PreStop hooked is executed. Regardless of the outcome of the handler, the \
        container will eventually terminate within the Pod's termination grace period. \
        Other management of the container blocks until the hook completes or until the \
        termination grace period is reached. More info: \
        https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks  # noqa
    :type pre_stop: Handler
    """

    def __init__(self, post_start: Handler, pre_stop: Handler):
        self.postStart = post_start
        self.preStop = pre_stop


class ContainerPort(HelmYaml):
    """
    :param container_port:Number of port to expose on the pod's IP address. This must \
        be a valid port number, 0 < x < 65536.
    :type container_port: int
    :param host_ip:What host IP to bind the external port to.
    :type host_ip: str
    :param host_port:Number of port to expose on the host. If specified, this must be \
        a valid port number, 0 < x < 65536. If HostNetwork is specified, this must \
        match ContainerPort. Most containers do not need this.
    :type host_port: Optional[int]
    :param name:If specified, this must be an IANA_SVC_NAME and unique within the pod. \
        Each named port in a pod must have a unique name. Name for the port that can \
        be referred to by services.
    :type name: Optional[str]
    :param protocol:Protocol for port. Must be UDP, TCP, or SCTP. Defaults to "TCP".
    :type protocol: Optional[str]
    """

    def __init__(
        self,
        container_port: int,
        host_ip: str,
        host_port: Optional[int] = None,
        name: Optional[str] = None,
        protocol: Optional[str] = None,
    ):
        self.containerPort = container_port
        self.hostIP = host_ip
        self.hostPort = host_port
        self.name = name
        self.protocol = protocol


class VolumeMount(HelmYaml):
    """
    :param name:This must match the Name of a Volume.
    :type name: str
    :param mount_path:Path within the container at which the volume should be mounted. \
         Must not contain ':'.
    :type mount_path: str
    :param mount_propagation:mountPropagation determines how mounts are propagated \
        from the host to container and the other way around. When not set, \
        MountPropagationNone is used. This field is beta in 1.10.
    :type mount_propagation: str
    :param read_only:Mounted read-only if true, read-write otherwise (false or \
        unspecified). Defaults to false.
    :type read_only: Optional[bool]
    :param sub_path:Path within the volume from which the container's volume should be \
        mounted. Defaults to "" (volume's root).
    :type sub_path: Optional[str]
    :param sub_path_expr:Expanded path within the volume from which the container's \
        volume should be mounted. Behaves similarly to SubPath but environment \
        variable references $(VAR_NAME) are expanded using the container's \
        environment. Defaults to "" (volume's root). SubPathExpr and SubPath are \
        mutually exclusive.
    :type sub_path_expr: Optional[str]
    """

    def __init__(
        self,
        name: str,
        mount_path: str,
        mount_propagation: str,
        read_only: Optional[bool] = None,
        sub_path: Optional[str] = None,
        sub_path_expr: Optional[str] = None,
    ):
        self.name = name
        self.mountPath = mount_path
        self.mountPropagation = mount_propagation
        self.readOnly = read_only
        self.subPath = sub_path
        self.subPathExpr = sub_path_expr


class Probe(HelmYaml):
    """
    :param exec:One and only one of the following should be specified. Exec specifies \
        the action to take.
    :type exec: ExecAction
    :param http_get:HTTPGet specifies the http request to perform.
    :type http_get: HTTPGetAction
    :param initial_delay_seconds:Number of seconds after the container has started \
        before liveness probes are initiated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type initial_delay_seconds: int
    :param period_seconds:How often (in seconds) to perform the probe. Default to 10 \
        seconds. Minimum value is 1.
    :type period_seconds: int
    :param tcp_socket:TCPSocket specifies an action involving a TCP port. TCP hooks \
        not yet supported
    :type tcp_socket: TCPSocketAction
    :param failure_threshold:Minimum consecutive failures for the probe to be \
        considered failed after having succeeded. Defaults to 3. Minimum value is 1.
    :type failure_threshold: Optional[int]
    :param success_threshold:Minimum consecutive successes for the probe to be \
        considered successful after having failed. Defaults to 1. Must be 1 for \
        liveness and startup. Minimum value is 1.
    :type success_threshold: Optional[int]
    :param timeout_seconds:Number of seconds after which the probe times out. Defaults \
        to 1 second. Minimum value is 1. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type timeout_seconds: Optional[int]
    """

    def __init__(
        self,
        exec: ExecAction,
        http_get: HTTPGetAction,
        initial_delay_seconds: int,
        period_seconds: int,
        tcp_socket: TCPSocketAction,
        failure_threshold: Optional[int] = None,
        success_threshold: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
    ):
        self.exec = exec
        self.httpGet = http_get
        self.initialDelaySeconds = initial_delay_seconds
        self.periodSeconds = period_seconds
        self.tcpSocket = tcp_socket
        self.failureThreshold = failure_threshold
        self.successThreshold = success_threshold
        self.timeoutSeconds = timeout_seconds


class Container(HelmYaml):
    """
    :param name:Name of the container specified as a DNS_LABEL. Each container in a \
        pod must have a unique name (DNS_LABEL). Cannot be updated.
    :type name: str
    :param args:Arguments to the entrypoint. The docker image's CMD is used if this is \
        not provided. Variable references $(VAR_NAME) are expanded using the \
        container's environment. If a variable cannot be resolved, the reference in \
        the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with \
        a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, \
        regardless of whether the variable exists or not. Cannot be updated. More \
        info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type args: Optional[List[str]]
    :param command:Entrypoint array. Not executed within a shell. The docker image's \
        ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) \
        are expanded using the container's environment. If a variable cannot be \
        resolved, the reference in the input string will be unchanged. The $(VAR_NAME) \
        syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references \
        will never be expanded, regardless of whether the variable exists or not. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type command: Optional[List[str]]
    :param env:List of environment variables to set in the container. Cannot be \
        updated.
    :type env: Optional[List[EnvVar]]
    :param env_from:List of sources to populate environment variables in the \
        container. The keys defined within a source must be a C_IDENTIFIER. All \
        invalid keys will be reported as an event when the container is starting. When \
        a key exists in multiple sources, the value associated with the last source \
        will take precedence. Values defined by an Env with a duplicate key will take \
        precedence. Cannot be updated.
    :type env_from: Optional[List[EnvFromSource]]
    :param image:Docker image name. More info: \
        https://kubernetes.io/docs/concepts/containers/images This field is optional \
        to allow higher level config management to default or override container \
        images in workload controllers like Deployments and StatefulSets.
    :type image: Optional[str]
    :param image_pull_policy:Image pull policy. One of Always, Never, IfNotPresent. \
        Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/containers/images#updating-images
    :type image_pull_policy: Optional[str]
    :param lifecycle:Actions that the management system should take in response to \
        container lifecycle events. Cannot be updated.
    :type lifecycle: Optional[Lifecycle]
    :param liveness_probe:Periodic probe of container liveness. Container will be \
        restarted if the probe fails. Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type liveness_probe: Optional[Probe]
    :param ports:List of ports to expose from the container. Exposing a port here \
        gives the system additional information about the network connections a \
        container uses, but is primarily informational. Not specifying a port here \
        DOES NOT prevent that port from being exposed. Any port which is listening on \
        the default "0.0.0.0" address inside a container will be accessible from the \
        network. Cannot be updated.
    :type ports: Optional[List[ContainerPort]]
    :param readiness_probe:Periodic probe of container service readiness. Container \
        will be removed from service endpoints if the probe fails. Cannot be updated. \
        More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type readiness_probe: Optional[Probe]
    :param resources:Compute Resources required by this container. Cannot be updated. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type resources: Optional[ResourceRequirements]
    :param security_context:Security options the pod should run with. More info: \
        https://kubernetes.io/docs/concepts/policy/security-context/ More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
    :type security_context: Optional[SecurityContext]
    :param startup_probe:StartupProbe indicates that the Pod has successfully \
        initialized. If specified, no other probes are executed until this completes \
        successfully. If this probe fails, the Pod will be restarted, just as if the \
        livenessProbe failed. This can be used to provide different probe parameters \
        at the beginning of a Pod's lifecycle, when it might take a long time to load \
        data or warm a cache, than during steady-state operation. This cannot be \
        updated. This is a beta feature enabled by the StartupProbe feature flag. More \
        info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type startup_probe: Optional[Probe]
    :param stdin:Whether this container should allocate a buffer for stdin in the \
        container runtime. If this is not set, reads from stdin in the container will \
        always result in EOF. Default is false.
    :type stdin: Optional[bool]
    :param stdin_once:Whether the container runtime should close the stdin channel \
        after it has been opened by a single attach. When stdin is true the stdin \
        stream will remain open across multiple attach sessions. If stdinOnce is set \
        to true, stdin is opened on container start, is empty until the first client \
        attaches to stdin, and then remains open and accepts data until the client \
        disconnects, at which time stdin is closed and remains closed until the \
        container is restarted. If this flag is false, a container processes that \
        reads from stdin will never receive an EOF. Default is false
    :type stdin_once: Optional[bool]
    :param termination_message_path:Optional: Path at which the file to which the \
        container's termination message will be written is mounted into the \
        container's filesystem. Message written is intended to be brief final status, \
        such as an assertion failure message. Will be truncated by the node if greater \
        than 4096 bytes. The total message length across all containers will be \
        limited to 12kb. Defaults to /dev/termination-log. Cannot be updated.
    :type termination_message_path: Optional[str]
    :param termination_message_policy:Indicate how the termination message should be \
        populated. File will use the contents of terminationMessagePath to populate \
        the container status message on both success and failure. \
        FallbackToLogsOnError will use the last chunk of container log output if the \
        termination message file is empty and the container exited with an error. The \
        log output is limited to 2048 bytes or 80 lines, whichever is smaller. \
        Defaults to File. Cannot be updated.
    :type termination_message_policy: Optional[str]
    :param tty:Whether this container should allocate a TTY for itself, also requires \
        'stdin' to be true. Default is false.
    :type tty: Optional[bool]
    :param volume_devices:volumeDevices is the list of block devices to be used by the \
        container.
    :type volume_devices: Optional[List[VolumeDevice]]
    :param volume_mounts:Pod volumes to mount into the container's filesystem. Cannot \
        be updated.
    :type volume_mounts: Optional[List[VolumeMount]]
    :param working_dir:Container's working directory. If not specified, the container \
        runtime's default will be used, which might be configured in the container \
        image. Cannot be updated.
    :type working_dir: Optional[str]
    """

    def __init__(
        self,
        name: str,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[EnvVar]] = None,
        env_from: Optional[List[EnvFromSource]] = None,
        image: Optional[str] = None,
        image_pull_policy: Optional[str] = None,
        lifecycle: Optional[Lifecycle] = None,
        liveness_probe: Optional[Probe] = None,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[Probe] = None,
        resources: Optional[ResourceRequirements] = None,
        security_context: Optional[SecurityContext] = None,
        startup_probe: Optional[Probe] = None,
        stdin: Optional[bool] = None,
        stdin_once: Optional[bool] = None,
        termination_message_path: Optional[str] = None,
        termination_message_policy: Optional[str] = None,
        tty: Optional[bool] = None,
        volume_devices: Optional[List[VolumeDevice]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        working_dir: Optional[str] = None,
    ):
        self.name = name
        self.args = args
        self.command = command
        self.env = env
        self.envFrom = env_from
        self.image = image
        self.imagePullPolicy = image_pull_policy
        self.lifecycle = lifecycle
        self.livenessProbe = liveness_probe
        self.ports = ports
        self.readinessProbe = readiness_probe
        self.resources = resources
        self.securityContext = security_context
        self.startupProbe = startup_probe
        self.stdin = stdin
        self.stdinOnce = stdin_once
        self.terminationMessagePath = termination_message_path
        self.terminationMessagePolicy = termination_message_policy
        self.tty = tty
        self.volumeDevices = volume_devices
        self.volumeMounts = volume_mounts
        self.workingDir = working_dir


class HostAlias(HelmYaml):
    """
    :param hostnames:Hostnames for the above IP address.
    :type hostnames: List[str]
    :param ip:IP address of the host file entry.
    :type ip: str
    """

    def __init__(self, hostnames: List[str], ip: str):
        self.hostnames = hostnames
        self.ip = ip


class Sysctl(HelmYaml):
    """
    :param name:Name of a property to set
    :type name: str
    :param value:Value of a property to set
    :type value: str
    """

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class PodSecurityContext(HelmYaml):
    """
    :param fs_group:A special supplemental group that applies to all containers in a \
        pod. Some volume types allow the Kubelet to change the ownership of that \
        volume to be owned by the pod:  1. The owning GID will be the FSGroup 2. The \
        setgid bit is set (new files created in the volume will be owned by FSGroup) \
        3. The permission bits are OR'd with rw-rw----  If unset, the Kubelet will not \
        modify the ownership and permissions of any volume.
    :type fs_group: int
    :param run_as_group:The GID to run the entrypoint of the container process. Uses \
        runtime default if unset. May also be set in SecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence for that container.
    :type run_as_group: int
    :param run_as_non_root:Indicates that the container must run as a non-root user. \
        If true, the Kubelet will validate the image at runtime to ensure that it does \
        not run as UID 0 (root) and fail to start the container if it does. If unset \
        or false, no such validation will be performed. May also be set in \
        SecurityContext.  If set in both SecurityContext and PodSecurityContext, the \
        value specified in SecurityContext takes precedence.
    :type run_as_non_root: bool
    :param se_linux_options:The SELinux context to be applied to all containers. If \
        unspecified, the container runtime will allocate a random SELinux context for \
        each container.  May also be set in SecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence for that container.
    :type se_linux_options: SELinuxOptions
    :param supplemental_groups:A list of groups applied to the first process run in \
        each container, in addition to the container's primary GID.  If unspecified, \
        no groups will be added to any container.
    :type supplemental_groups: List[int]
    :param sysctls:Sysctls hold a list of namespaced sysctls used for the pod. Pods \
        with unsupported sysctls (by the container runtime) might fail to launch.
    :type sysctls: List[Sysctl]
    :param windows_options:The Windows specific settings applied to all containers. If \
        unspecified, the options within a container's SecurityContext will be used. If \
        set in both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :type windows_options: WindowsSecurityContextOptions
    :param fs_group_change_policy:fsGroupChangePolicy defines behavior of changing \
        ownership and permission of the volume before being exposed inside Pod. This \
        field will only apply to volume types which support fsGroup based \
        ownership(and permissions). It will have no effect on ephemeral volume types \
        such as: secret, configmaps and emptydir. Valid values are "OnRootMismatch" \
        and "Always". If not specified defaults to "Always".
    :type fs_group_change_policy: Optional[str]
    :param run_as_user:The UID to run the entrypoint of the container process. \
        Defaults to user specified in image metadata if unspecified. May also be set \
        in SecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence for that container.
    :type run_as_user: Optional[int]
    """

    def __init__(
        self,
        fs_group: int,
        run_as_group: int,
        run_as_non_root: bool,
        se_linux_options: SELinuxOptions,
        supplemental_groups: List[int],
        sysctls: List[Sysctl],
        windows_options: WindowsSecurityContextOptions,
        fs_group_change_policy: Optional[str] = None,
        run_as_user: Optional[int] = None,
    ):
        self.fsGroup = fs_group
        self.runAsGroup = run_as_group
        self.runAsNonRoot = run_as_non_root
        self.seLinuxOptions = se_linux_options
        self.supplementalGroups = supplemental_groups
        self.sysctls = sysctls
        self.windowsOptions = windows_options
        self.fsGroupChangePolicy = fs_group_change_policy
        self.runAsUser = run_as_user


class TopologySpreadConstraint(HelmYaml):
    """
    :param label_selector:LabelSelector is used to find matching pods. Pods that match \
        this label selector are counted to determine the number of pods in their \
        corresponding topology domain.
    :type label_selector: LabelSelector
    :param max_skew:MaxSkew describes the degree to which pods may be unevenly \
        distributed. It's the maximum permitted difference between the number of \
        matching pods in any two topology domains of a given topology type. For \
        example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same \
        labelSelector spread as 1/1/0: | zone1 | zone2 | zone3 | |   P   |   P   |     \
          | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become \
        1/1/1; scheduling it onto zone1(zone2) would make the ActualSkew(2-0) on \
        zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be \
        scheduled onto any zone. It's a required field. Default value is 1 and 0 is \
        not allowed.
    :type max_skew: int
    :param topology_key:TopologyKey is the key of node labels. Nodes that have a label \
        with this key and identical values are considered to be in the same topology. \
        We consider each <key, value> as a "bucket", and try to put balanced number of \
        pods into each bucket. It's a required field.
    :type topology_key: str
    :param when_unsatisfiable:WhenUnsatisfiable indicates how to deal with a pod if it \
        doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the \
        scheduler not to schedule it - ScheduleAnyway tells the scheduler to still \
        schedule it It's considered as "Unsatisfiable" if and only if placing incoming \
        pod on any topology violates "MaxSkew". For example, in a 3-zone cluster, \
        MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: | \
        zone1 | zone2 | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set \
        to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become \
        3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other \
        words, the cluster can still be imbalanced, but scheduler won't make it *more* \
        imbalanced. It's a required field.
    :type when_unsatisfiable: str
    """

    def __init__(
        self,
        label_selector: LabelSelector,
        max_skew: int,
        topology_key: str,
        when_unsatisfiable: str,
    ):
        self.labelSelector = label_selector
        self.maxSkew = max_skew
        self.topologyKey = topology_key
        self.whenUnsatisfiable = when_unsatisfiable


class PodDNSConfigOption(HelmYaml):
    """
    :param name:Required.
    :type name: str
    :param value:None
    :type value: str
    """

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class PodDNSConfig(HelmYaml):
    """
    :param nameservers:A list of DNS name server IP addresses. This will be appended \
        to the base nameservers generated from DNSPolicy. Duplicated nameservers will \
        be removed.
    :type nameservers: List[str]
    :param options:A list of DNS resolver options. This will be merged with the base \
        options generated from DNSPolicy. Duplicated entries will be removed. \
        Resolution options given in Options will override those that appear in the \
        base DNSPolicy.
    :type options: List[PodDNSConfigOption]
    :param searches:A list of DNS search domains for host-name lookup. This will be \
        appended to the base search paths generated from DNSPolicy. Duplicated search \
        paths will be removed.
    :type searches: List[str]
    """

    def __init__(
        self,
        nameservers: List[str],
        options: List[PodDNSConfigOption],
        searches: List[str],
    ):
        self.nameservers = nameservers
        self.options = options
        self.searches = searches


class EphemeralContainer(HelmYaml):
    """
    :param name:Name of the ephemeral container specified as a DNS_LABEL. This name \
        must be unique among all containers, init containers and ephemeral containers.
    :type name: str
    :param image:Docker image name. More info: \
        https://kubernetes.io/docs/concepts/containers/images
    :type image: str
    :param ports:Ports are not allowed for ephemeral containers.
    :type ports: List[ContainerPort]
    :param resources:Resources are not allowed for ephemeral containers. Ephemeral \
        containers use spare resources already allocated to the pod.
    :type resources: ResourceRequirements
    :param startup_probe:Probes are not allowed for ephemeral containers.
    :type startup_probe: Probe
    :param target_container_name:If set, the name of the container from PodSpec that \
        this ephemeral container targets. The ephemeral container will be run in the \
        namespaces (IPC, PID, etc) of this container. If not set then the ephemeral \
        container is run in whatever namespaces are shared for the pod. Note that the \
        container runtime must support this feature.
    :type target_container_name: str
    :param args:Arguments to the entrypoint. The docker image's CMD is used if this is \
        not provided. Variable references $(VAR_NAME) are expanded using the \
        container's environment. If a variable cannot be resolved, the reference in \
        the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with \
        a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, \
        regardless of whether the variable exists or not. Cannot be updated. More \
        info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type args: Optional[List[str]]
    :param command:Entrypoint array. Not executed within a shell. The docker image's \
        ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) \
        are expanded using the container's environment. If a variable cannot be \
        resolved, the reference in the input string will be unchanged. The $(VAR_NAME) \
        syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references \
        will never be expanded, regardless of whether the variable exists or not. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type command: Optional[List[str]]
    :param env:List of environment variables to set in the container. Cannot be \
        updated.
    :type env: Optional[List[EnvVar]]
    :param env_from:List of sources to populate environment variables in the \
        container. The keys defined within a source must be a C_IDENTIFIER. All \
        invalid keys will be reported as an event when the container is starting. When \
        a key exists in multiple sources, the value associated with the last source \
        will take precedence. Values defined by an Env with a duplicate key will take \
        precedence. Cannot be updated.
    :type env_from: Optional[List[EnvFromSource]]
    :param image_pull_policy:Image pull policy. One of Always, Never, IfNotPresent. \
        Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/containers/images#updating-images
    :type image_pull_policy: Optional[str]
    :param lifecycle:Lifecycle is not allowed for ephemeral containers.
    :type lifecycle: Optional[Lifecycle]
    :param liveness_probe:Probes are not allowed for ephemeral containers.
    :type liveness_probe: Optional[Probe]
    :param readiness_probe:Probes are not allowed for ephemeral containers.
    :type readiness_probe: Optional[Probe]
    :param security_context:SecurityContext is not allowed for ephemeral containers.
    :type security_context: Optional[SecurityContext]
    :param stdin:Whether this container should allocate a buffer for stdin in the \
        container runtime. If this is not set, reads from stdin in the container will \
        always result in EOF. Default is false.
    :type stdin: Optional[bool]
    :param stdin_once:Whether the container runtime should close the stdin channel \
        after it has been opened by a single attach. When stdin is true the stdin \
        stream will remain open across multiple attach sessions. If stdinOnce is set \
        to true, stdin is opened on container start, is empty until the first client \
        attaches to stdin, and then remains open and accepts data until the client \
        disconnects, at which time stdin is closed and remains closed until the \
        container is restarted. If this flag is false, a container processes that \
        reads from stdin will never receive an EOF. Default is false
    :type stdin_once: Optional[bool]
    :param termination_message_path:Optional: Path at which the file to which the \
        container's termination message will be written is mounted into the \
        container's filesystem. Message written is intended to be brief final status, \
        such as an assertion failure message. Will be truncated by the node if greater \
        than 4096 bytes. The total message length across all containers will be \
        limited to 12kb. Defaults to /dev/termination-log. Cannot be updated.
    :type termination_message_path: Optional[str]
    :param termination_message_policy:Indicate how the termination message should be \
        populated. File will use the contents of terminationMessagePath to populate \
        the container status message on both success and failure. \
        FallbackToLogsOnError will use the last chunk of container log output if the \
        termination message file is empty and the container exited with an error. The \
        log output is limited to 2048 bytes or 80 lines, whichever is smaller. \
        Defaults to File. Cannot be updated.
    :type termination_message_policy: Optional[str]
    :param tty:Whether this container should allocate a TTY for itself, also requires \
        'stdin' to be true. Default is false.
    :type tty: Optional[bool]
    :param volume_devices:volumeDevices is the list of block devices to be used by the \
        container.
    :type volume_devices: Optional[List[VolumeDevice]]
    :param volume_mounts:Pod volumes to mount into the container's filesystem. Cannot \
        be updated.
    :type volume_mounts: Optional[List[VolumeMount]]
    :param working_dir:Container's working directory. If not specified, the container \
        runtime's default will be used, which might be configured in the container \
        image. Cannot be updated.
    :type working_dir: Optional[str]
    """

    def __init__(
        self,
        name: str,
        image: str,
        ports: List[ContainerPort],
        resources: ResourceRequirements,
        startup_probe: Probe,
        target_container_name: str,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[EnvVar]] = None,
        env_from: Optional[List[EnvFromSource]] = None,
        image_pull_policy: Optional[str] = None,
        lifecycle: Optional[Lifecycle] = None,
        liveness_probe: Optional[Probe] = None,
        readiness_probe: Optional[Probe] = None,
        security_context: Optional[SecurityContext] = None,
        stdin: Optional[bool] = None,
        stdin_once: Optional[bool] = None,
        termination_message_path: Optional[str] = None,
        termination_message_policy: Optional[str] = None,
        tty: Optional[bool] = None,
        volume_devices: Optional[List[VolumeDevice]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        working_dir: Optional[str] = None,
    ):
        self.name = name
        self.image = image
        self.ports = ports
        self.resources = resources
        self.startupProbe = startup_probe
        self.targetContainerName = target_container_name
        self.args = args
        self.command = command
        self.env = env
        self.envFrom = env_from
        self.imagePullPolicy = image_pull_policy
        self.lifecycle = lifecycle
        self.livenessProbe = liveness_probe
        self.readinessProbe = readiness_probe
        self.securityContext = security_context
        self.stdin = stdin
        self.stdinOnce = stdin_once
        self.terminationMessagePath = termination_message_path
        self.terminationMessagePolicy = termination_message_policy
        self.tty = tty
        self.volumeDevices = volume_devices
        self.volumeMounts = volume_mounts
        self.workingDir = working_dir


class LocalObjectReference(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    """

    def __init__(self, name: str):
        self.name = name


class DownwardAPIVolumeSource(HelmYaml):
    """
    :param items:Items is a list of downward API volume file
    :type items: List[DownwardAPIVolumeFile]
    :param default_mode:Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    :type default_mode: Optional[int]
    """

    def __init__(
        self, items: List[DownwardAPIVolumeFile], default_mode: Optional[int] = None
    ):
        self.items = items
        self.defaultMode = default_mode


class ScaleIOVolumeSource(HelmYaml):
    """
    :param gateway:The host address of the ScaleIO API Gateway.
    :type gateway: str
    :param protection_domain:The name of the ScaleIO Protection Domain for the \
        configured storage.
    :type protection_domain: str
    :param ssl_enabled:Flag to enable/disable SSL communication with Gateway, default \
        false
    :type ssl_enabled: bool
    :param storage_pool:The ScaleIO Storage Pool associated with the protection \
        domain.
    :type storage_pool: str
    :param system:The name of the storage system as configured in ScaleIO.
    :type system: str
    :param volume_name:The name of a volume already created in the ScaleIO system that \
        is associated with this volume source.
    :type volume_name: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Default is "xfs".
    :type fs_type: Optional[str]
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef references to the secret for ScaleIO user and other \
        sensitive information. If this is not provided, Login operation will fail.
    :type secret_ref: Optional[LocalObjectReference]
    :param storage_mode:Indicates whether the storage for a volume should be \
        ThickProvisioned or ThinProvisioned. Default is ThinProvisioned.
    :type storage_mode: Optional[str]
    """

    def __init__(
        self,
        gateway: str,
        protection_domain: str,
        ssl_enabled: bool,
        storage_pool: str,
        system: str,
        volume_name: str,
        fs_type: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        storage_mode: Optional[str] = None,
    ):
        self.gateway = gateway
        self.protectionDomain = protection_domain
        self.sslEnabled = ssl_enabled
        self.storagePool = storage_pool
        self.system = system
        self.volumeName = volume_name
        self.fsType = fs_type
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.storageMode = storage_mode


class CephFSVolumeSource(HelmYaml):
    """
    :param monitors:Required: Monitors is a collection of Ceph monitors More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type monitors: List[str]
    :param path:Optional: Used as the mounted root, rather than the full Ceph tree, \
        default is /
    :type path: Optional[str]
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type read_only: Optional[bool]
    :param secret_file:Optional: SecretFile is the path to key ring for User, default \
        is /etc/ceph/user.secret More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type secret_file: Optional[str]
    :param secret_ref:Optional: SecretRef is reference to the authentication secret \
        for User, default is empty. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type secret_ref: Optional[LocalObjectReference]
    :param user:Optional: User is the rados user name, default is admin More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type user: Optional[str]
    """

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_file: Optional[str] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        self.monitors = monitors
        self.path = path
        self.readOnly = read_only
        self.secretFile = secret_file
        self.secretRef = secret_ref
        self.user = user


class HostPathVolumeSource(HelmYaml):
    """
    :param path:Path of the directory on the host. If the path is a symlink, it will \
        follow the link to the real path. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :type path: str
    :param type:Type for HostPath Volume Defaults to "" More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :type type: Optional[str]
    """

    def __init__(self, path: str, type: Optional[str] = None):
        self.path = path
        self.type = type


class CinderVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly \
        inferred to be "ext4" if unspecified. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type fs_type: str
    :param volume_id:volume id used to identify the volume in cinder. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type volume_id: str
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type read_only: Optional[bool]
    :param secret_ref:Optional: points to a secret object containing parameters used \
        to connect to OpenStack.
    :type secret_ref: Optional[LocalObjectReference]
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only
        self.secretRef = secret_ref


class PortworxVolumeSource(HelmYaml):
    """
    :param fs_type:FSType represents the filesystem type to mount Must be a filesystem \
        type supported by the host operating system. Ex. "ext4", "xfs". Implicitly \
        inferred to be "ext4" if unspecified.
    :type fs_type: str
    :param volume_id:VolumeID uniquely identifies a Portworx volume
    :type volume_id: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    """

    def __init__(self, fs_type: str, volume_id: str, read_only: Optional[bool] = None):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only


class CSIVolumeSource(HelmYaml):
    """
    :param driver:Driver is the name of the CSI driver that handles this volume. \
        Consult with your admin for the correct name as registered in the cluster.
    :type driver: str
    :param fs_type:Filesystem type to mount. Ex. "ext4", "xfs", "ntfs". If not \
        provided, the empty value is passed to the associated CSI driver which will \
        determine the default filesystem to apply.
    :type fs_type: str
    :param volume_attributes:VolumeAttributes stores driver-specific properties that \
        are passed to the CSI driver. Consult your driver's documentation for \
        supported values.
    :type volume_attributes: dict
    :param node_publish_secret_ref:NodePublishSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodePublishVolume and NodeUnpublishVolume calls. This field is \
        optional, and  may be empty if no secret is required. If the secret object \
        contains more than one secret, all secret references are passed.
    :type node_publish_secret_ref: Optional[LocalObjectReference]
    :param read_only:Specifies a read-only configuration for the volume. Defaults to \
        false (read/write).
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        volume_attributes: dict,
        node_publish_secret_ref: Optional[LocalObjectReference] = None,
        read_only: Optional[bool] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.volumeAttributes = volume_attributes
        self.nodePublishSecretRef = node_publish_secret_ref
        self.readOnly = read_only


class StorageOSVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param volume_name:VolumeName is the human-readable name of the StorageOS volume.  \
        Volume names are only unique within a namespace.
    :type volume_name: str
    :param volume_namespace:VolumeNamespace specifies the scope of the volume within \
        StorageOS.  If no namespace is specified then the Pod's namespace will be \
        used.  This allows the Kubernetes name scoping to be mirrored within StorageOS \
        for tighter integration. Set VolumeName to any name to override the default \
        behaviour. Set to "default" if you are not using namespaces within StorageOS. \
        Namespaces that do not pre-exist within StorageOS will be created.
    :type volume_namespace: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef specifies the secret to use for obtaining the \
        StorageOS API credentials.  If not specified, default values will be \
        attempted.
    :type secret_ref: Optional[LocalObjectReference]
    """

    def __init__(
        self,
        fs_type: str,
        volume_name: str,
        volume_namespace: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeName = volume_name
        self.volumeNamespace = volume_namespace
        self.readOnly = read_only
        self.secretRef = secret_ref


class PhotonPersistentDiskVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param pd_id:ID that identifies Photon Controller persistent disk
    :type pd_id: str
    """

    def __init__(self, fs_type: str, pd_id: str):
        self.fsType = fs_type
        self.pdID = pd_id


class GlusterfsVolumeSource(HelmYaml):
    """
    :param endpoints:EndpointsName is the endpoint name that details Glusterfs \
        topology. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type endpoints: str
    :param path:Path is the Glusterfs volume path. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type path: str
    :param read_only:ReadOnly here will force the Glusterfs volume to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type read_only: Optional[bool]
    """

    def __init__(self, endpoints: str, path: str, read_only: Optional[bool] = None):
        self.endpoints = endpoints
        self.path = path
        self.readOnly = read_only


class AzureDiskVolumeSource(KubernetesBaseObject):
    """
    :param caching_mode:Host Caching mode: None, Read Only, Read Write.
    :type caching_mode: str
    :param disk_name:The Name of the data disk in the blob storage
    :type disk_name: str
    :param disk_uri:The URI the data disk in the blob storage
    :type disk_uri: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        caching_mode: str,
        disk_name: str,
        disk_uri: str,
        fs_type: str,
        read_only: Optional[bool] = None,
    ):
        self.cachingMode = caching_mode
        self.diskName = disk_name
        self.diskURI = disk_uri
        self.fsType = fs_type
        self.readOnly = read_only


class AzureFileVolumeSource(HelmYaml):
    """
    :param secret_name:the name of secret that contains Azure Storage Account Name and \
        Key
    :type secret_name: str
    :param share_name:Share Name
    :type share_name: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    """

    def __init__(
        self, secret_name: str, share_name: str, read_only: Optional[bool] = None
    ):
        self.secretName = secret_name
        self.shareName = share_name
        self.readOnly = read_only


class SecretVolumeSource(HelmYaml):
    """
    :param optional:Specify whether the Secret or its keys must be defined
    :type optional: bool
    :param secret_name:Name of the secret in the pod's namespace to use. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#secret
    :type secret_name: str
    :param default_mode:Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    :type default_mode: Optional[int]
    :param items:If unspecified, each key-value pair in the Data field of the \
        referenced Secret will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the Secret, the volume setup will \
        error unless it is marked optional. Paths must be relative and may not contain \
        the '..' path or start with '..'.
    :type items: Optional[List[KeyToPath]]
    """

    def __init__(
        self,
        optional: bool,
        secret_name: str,
        default_mode: Optional[int] = None,
        items: Optional[List[KeyToPath]] = None,
    ):
        self.optional = optional
        self.secretName = secret_name
        self.defaultMode = default_mode
        self.items = items


class EmptyDirVolumeSource(HelmYaml):
    """
    :param medium:What type of storage medium should back this directory. The default \
        is "" which means to use the node's default medium. Must be an empty string \
        (default) or Memory. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#emptydir
    :type medium: Optional[str]
    :param size_limit:Total amount of local storage required for this EmptyDir volume. \
        The size limit is also applicable for memory medium. The maximum usage on \
        memory medium EmptyDir would be the minimum value between the SizeLimit \
        specified here and the sum of memory limits of all containers in a pod. The \
        default is nil which means that the limit is undefined. More info: \
        http://kubernetes.io/docs/user-guide/volumes#emptydir
    :type size_limit: Optional[str]
    """

    def __init__(self, medium: Optional[str] = None, size_limit: Optional[str] = None):
        self.medium = medium
        self.sizeLimit = size_limit


class QuobyteVolumeSource(HelmYaml):
    """
    :param registry:Registry represents a single or multiple Quobyte Registry services \
        specified as a string as host:port pair (multiple entries are separated with \
        commas) which acts as the central registry for volumes
    :type registry: str
    :param tenant:Tenant owning the given Quobyte volume in the Backend Used with \
        dynamically provisioned Quobyte volumes, value is set by the plugin
    :type tenant: str
    :param volume:Volume is a string that references an already created Quobyte volume \
        by name.
    :type volume: str
    :param group:Group to map volume access to Default is no group
    :type group: Optional[str]
    :param read_only:ReadOnly here will force the Quobyte volume to be mounted with \
        read-only permissions. Defaults to false.
    :type read_only: Optional[bool]
    :param user:User to map volume access to Defaults to serivceaccount user
    :type user: Optional[str]
    """

    def __init__(
        self,
        registry: str,
        tenant: str,
        volume: str,
        group: Optional[str] = None,
        read_only: Optional[bool] = None,
        user: Optional[str] = None,
    ):
        self.registry = registry
        self.tenant = tenant
        self.volume = volume
        self.group = group
        self.readOnly = read_only
        self.user = user


class RBDVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#rbd
    :type fs_type: str
    :param image:The rados image name. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type image: str
    :param monitors:A collection of Ceph monitors. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type monitors: List[str]
    :param keyring:Keyring is the path to key ring for RBDUser. Default is \
        /etc/ceph/keyring. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type keyring: Optional[str]
    :param pool:The rados pool name. Default is rbd. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type pool: Optional[str]
    :param read_only:ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef is name of the authentication secret for RBDUser. If \
        provided overrides keyring. Default is nil. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type secret_ref: Optional[LocalObjectReference]
    :param user:The rados user name. Default is admin. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type user: Optional[str]
    """

    def __init__(
        self,
        fs_type: str,
        image: str,
        monitors: List[str],
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        self.fsType = fs_type
        self.image = image
        self.monitors = monitors
        self.keyring = keyring
        self.pool = pool
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.user = user


class ServiceAccountTokenProjection(HelmYaml):
    """
    :param path:Path is the path relative to the mount point of the file to project \
        the token into.
    :type path: str
    :param audience:Audience is the intended audience of the token. A recipient of a \
        token must identify itself with an identifier specified in the audience of the \
        token, and otherwise should reject the token. The audience defaults to the \
        identifier of the apiserver.
    :type audience: Optional[str]
    :param expiration_seconds:ExpirationSeconds is the requested duration of validity \
        of the service account token. As the token approaches expiration, the kubelet \
        volume plugin will proactively rotate the service account token. The kubelet \
        will start trying to rotate the token if the token is older than 80 percent of \
        its time to live or if the token is older than 24 hours.Defaults to 1 hour and \
        must be at least 10 minutes.
    :type expiration_seconds: Optional[int]
    """

    def __init__(
        self,
        path: str,
        audience: Optional[str] = None,
        expiration_seconds: Optional[int] = None,
    ):
        self.path = path
        self.audience = audience
        self.expirationSeconds = expiration_seconds


class ConfigMapProjection(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param optional:Specify whether the ConfigMap or its keys must be defined
    :type optional: bool
    :param items:If unspecified, each key-value pair in the Data field of the \
        referenced ConfigMap will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the ConfigMap, the volume setup \
        will error unless it is marked optional. Paths must be relative and may not \
        contain the '..' path or start with '..'.
    :type items: Optional[List[KeyToPath]]
    """

    def __init__(
        self, name: str, optional: bool, items: Optional[List[KeyToPath]] = None
    ):
        self.name = name
        self.optional = optional
        self.items = items


class VolumeProjection(HelmYaml):
    """
    :param config_map:information about the configMap data to project
    :type config_map: ConfigMapProjection
    :param downward_api:information about the downwardAPI data to project
    :type downward_api: DownwardAPIProjection
    :param secret:information about the secret data to project
    :type secret: SecretProjection
    :param service_account_token:information about the serviceAccountToken data to \
        project
    :type service_account_token: ServiceAccountTokenProjection
    """

    def __init__(
        self,
        config_map: ConfigMapProjection,
        downward_api: DownwardAPIProjection,
        secret: SecretProjection,
        service_account_token: ServiceAccountTokenProjection,
    ):
        self.configMap = config_map
        self.downwardAPI = downward_api
        self.secret = secret
        self.serviceAccountToken = service_account_token


class ProjectedVolumeSource(HelmYaml):
    """
    :param default_mode:Mode bits to use on created files by default. Must be a value \
        between 0 and 0777. Directories within the path are not affected by this \
        setting. This might be in conflict with other options that affect the file \
        mode, like fsGroup, and the result can be other mode bits set.
    :type default_mode: int
    :param sources:list of volume projections
    :type sources: List[VolumeProjection]
    """

    def __init__(self, default_mode: int, sources: List[VolumeProjection]):
        self.defaultMode = default_mode
        self.sources = sources


class VsphereVirtualDiskVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param storage_policy_id:Storage Policy Based Management (SPBM) profile ID \
        associated with the StoragePolicyName.
    :type storage_policy_id: str
    :param storage_policy_name:Storage Policy Based Management (SPBM) profile name.
    :type storage_policy_name: str
    :param volume_path:Path that identifies vSphere volume vmdk
    :type volume_path: str
    """

    def __init__(
        self,
        fs_type: str,
        storage_policy_id: str,
        storage_policy_name: str,
        volume_path: str,
    ):
        self.fsType = fs_type
        self.storagePolicyID = storage_policy_id
        self.storagePolicyName = storage_policy_name
        self.volumePath = volume_path


class FlockerVolumeSource(HelmYaml):
    """
    :param dataset_name:Name of the dataset stored as metadata -> name on the dataset \
        for Flocker should be considered as deprecated
    :type dataset_name: str
    :param dataset_uuid:UUID of the dataset. This is unique identifier of a Flocker \
        dataset
    :type dataset_uuid: str
    """

    def __init__(self, dataset_name: str, dataset_uuid: str):
        self.datasetName = dataset_name
        self.datasetUUID = dataset_uuid


class AWSElasticBlockStoreVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :type fs_type: str
    :param volume_id:Unique ID of the persistent disk resource in AWS (Amazon EBS \
        volume). More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :type volume_id: str
    :param partition:The partition in the volume that you want to mount. If omitted, \
        the default is to mount by volume name. Examples: For volume /dev/sda1, you \
        specify the partition as "1". Similarly, the volume partition for /dev/sda is \
        "0" (or you can leave the property empty).
    :type partition: Optional[int]
    :param read_only:Specify "true" to force and set the ReadOnly property in \
        VolumeMounts to "true". If omitted, the default is "false". More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        partition: Optional[int] = None,
        read_only: Optional[bool] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.partition = partition
        self.readOnly = read_only


class FlexVolumeSource(HelmYaml):
    """
    :param driver:Driver is the name of the driver to use for this volume.
    :type driver: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem \
        depends on FlexVolume script.
    :type fs_type: str
    :param options:Optional: Extra command options if any.
    :type options: Optional[dict]
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:Optional: SecretRef is reference to the secret object containing \
        sensitive information to pass to the plugin scripts. This may be empty if no \
        secret object is specified. If the secret object contains more than one \
        secret, all secrets are passed to the plugin scripts.
    :type secret_ref: Optional[LocalObjectReference]
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        options: Optional[dict] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.options = options
        self.readOnly = read_only
        self.secretRef = secret_ref


class FCVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param lun:Optional: FC target lun number
    :type lun: Optional[int]
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param target_wwns:Optional: FC target worldwide names (WWNs)
    :type target_wwns: Optional[List[str]]
    :param wwids:Optional: FC volume world wide identifiers (wwids) Either wwids or \
        combination of targetWWNs and lun must be set, but not both simultaneously.
    :type wwids: Optional[List[str]]
    """

    def __init__(
        self,
        fs_type: str,
        lun: Optional[int] = None,
        read_only: Optional[bool] = None,
        target_wwns: Optional[List[str]] = None,
        wwids: Optional[List[str]] = None,
    ):
        self.fsType = fs_type
        self.lun = lun
        self.readOnly = read_only
        self.targetWWNs = target_wwns
        self.wwids = wwids


class ISCSIVolumeSource(HelmYaml):
    """
    :param chap_auth_discovery:whether support iSCSI Discovery CHAP authentication
    :type chap_auth_discovery: bool
    :param chap_auth_session:whether support iSCSI Session CHAP authentication
    :type chap_auth_session: bool
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi
    :type fs_type: str
    :param initiator_name:Custom iSCSI Initiator Name. If initiatorName is specified \
        with iscsiInterface simultaneously, new iSCSI interface <target \
        portal>:<volume name> will be created for the connection.
    :type initiator_name: str
    :param iqn:Target iSCSI Qualified Name.
    :type iqn: str
    :param lun:iSCSI Target Lun number.
    :type lun: int
    :param portals:iSCSI Target Portal List. The portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :type portals: List[str]
    :param secret_ref:CHAP Secret for iSCSI target and initiator authentication
    :type secret_ref: LocalObjectReference
    :param target_portal:iSCSI Target Portal. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :type target_portal: str
    :param iscsi_interface:iSCSI Interface Name that uses an iSCSI transport. Defaults \
        to 'default' (tcp).
    :type iscsi_interface: Optional[str]
    :param read_only:ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false.
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        chap_auth_discovery: bool,
        chap_auth_session: bool,
        fs_type: str,
        initiator_name: str,
        iqn: str,
        lun: int,
        portals: List[str],
        secret_ref: LocalObjectReference,
        target_portal: str,
        iscsi_interface: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.chapAuthDiscovery = chap_auth_discovery
        self.chapAuthSession = chap_auth_session
        self.fsType = fs_type
        self.initiatorName = initiator_name
        self.iqn = iqn
        self.lun = lun
        self.portals = portals
        self.secretRef = secret_ref
        self.targetPortal = target_portal
        self.iscsiInterface = iscsi_interface
        self.readOnly = read_only


class GCEPersistentDiskVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type fs_type: str
    :param pd_name:Unique name of the PD resource in GCE. Used to identify the disk in \
        GCE. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type pd_name: str
    :param partition:The partition in the volume that you want to mount. If omitted, \
        the default is to mount by volume name. Examples: For volume /dev/sda1, you \
        specify the partition as "1". Similarly, the volume partition for /dev/sda is \
        "0" (or you can leave the property empty). More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type partition: Optional[int]
    :param read_only:ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        fs_type: str,
        pd_name: str,
        partition: Optional[int] = None,
        read_only: Optional[bool] = None,
    ):
        self.fsType = fs_type
        self.pdName = pd_name
        self.partition = partition
        self.readOnly = read_only


class NFSVolumeSource(HelmYaml):
    """
    :param path:Path that is exported by the NFS server. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :type path: str
    :param server:Server is the hostname or IP address of the NFS server. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :type server: str
    :param read_only:ReadOnly here will force the NFS export to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :type read_only: Optional[bool]
    """

    def __init__(self, path: str, server: str, read_only: Optional[bool] = None):
        self.path = path
        self.server = server
        self.readOnly = read_only


class ConfigMapVolumeSource(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param optional:Specify whether the ConfigMap or its keys must be defined
    :type optional: bool
    :param default_mode:Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    :type default_mode: Optional[int]
    :param items:If unspecified, each key-value pair in the Data field of the \
        referenced ConfigMap will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the ConfigMap, the volume setup \
        will error unless it is marked optional. Paths must be relative and may not \
        contain the '..' path or start with '..'.
    :type items: Optional[List[KeyToPath]]
    """

    def __init__(
        self,
        name: str,
        optional: bool,
        default_mode: Optional[int] = None,
        items: Optional[List[KeyToPath]] = None,
    ):
        self.name = name
        self.optional = optional
        self.defaultMode = default_mode
        self.items = items


class PersistentVolumeClaimVolumeSource(HelmYaml):
    """
    :param claim_name:ClaimName is the name of a PersistentVolumeClaim in the same \
        namespace as the pod using this volume. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :type claim_name: str
    :param read_only:Will force the ReadOnly setting in VolumeMounts. Default false.
    :type read_only: bool
    """

    def __init__(self, claim_name: str, read_only: bool):
        self.claimName = claim_name
        self.readOnly = read_only


class GitRepoVolumeSource(HelmYaml):
    """
    :param repository:Repository URL
    :type repository: str
    :param revision:Commit hash for the specified revision.
    :type revision: str
    :param directory:Target directory name. Must not contain or start with '..'.  If \
        '.' is supplied, the volume directory will be the git repository.  Otherwise, \
        if specified, the volume will contain the git repository in the subdirectory \
        with the given name.
    :type directory: Optional[str]
    """

    def __init__(self, repository: str, revision: str, directory: Optional[str] = None):
        self.repository = repository
        self.revision = revision
        self.directory = directory


class Volume(HelmYaml):
    """
    :param name:Volume's name. Must be a DNS_LABEL and unique within the pod. More \
        info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: str
    :param config_map:ConfigMap represents a configMap that should populate this \
        volume
    :type config_map: ConfigMapVolumeSource
    :param downward_api:DownwardAPI represents downward API about the pod that should \
        populate this volume
    :type downward_api: DownwardAPIVolumeSource
    :param empty_dir:EmptyDir represents a temporary directory that shares a pod's \
        lifetime. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#emptydir
    :type empty_dir: EmptyDirVolumeSource
    :param git_repo:GitRepo represents a git repository at a particular revision. \
        DEPRECATED: GitRepo is deprecated. To provision a container with a git repo, \
        mount an EmptyDir into an InitContainer that clones the repo using git, then \
        mount the EmptyDir into the Pod's container.
    :type git_repo: GitRepoVolumeSource
    :param host_path:HostPath represents a pre-existing file or directory on the host \
        machine that is directly exposed to the container. This is generally used for \
        system agents or other privileged things that are allowed to see the host \
        machine. Most containers will NOT need this. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :type host_path: HostPathVolumeSource
    :param persistent_volume_claim:PersistentVolumeClaimVolumeSource represents a \
        reference to a PersistentVolumeClaim in the same namespace. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :type persistent_volume_claim: PersistentVolumeClaimVolumeSource
    :param projected:Items for all in one resources secrets, configmaps, and downward \
        API
    :type projected: ProjectedVolumeSource
    :param secret:Secret represents a secret that should populate this volume. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#secret
    :type secret: SecretVolumeSource
    :param aws_elastic_block_store:AWSElasticBlockStore represents an AWS Disk \
        resource that is attached to a kubelet's host machine and then exposed to the \
        pod. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :type aws_elastic_block_store: Optional[AWSElasticBlockStoreVolumeSource]
    :param azure_disk:AzureDisk represents an Azure Data Disk mount on the host and \
        bind mount to the pod.
    :type azure_disk: Optional[AzureDiskVolumeSource]
    :param azure_file:AzureFile represents an Azure File Service mount on the host and \
        bind mount to the pod.
    :type azure_file: Optional[AzureFileVolumeSource]
    :param cephfs:CephFS represents a Ceph FS mount on the host that shares a pod's \
        lifetime
    :type cephfs: Optional[CephFSVolumeSource]
    :param cinder:Cinder represents a cinder volume attached and mounted on kubelets \
        host machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md
    :type cinder: Optional[CinderVolumeSource]
    :param csi:CSI (Container Storage Interface) represents storage that is handled by \
        an external CSI driver (Alpha feature).
    :type csi: Optional[CSIVolumeSource]
    :param fc:FC represents a Fibre Channel resource that is attached to a kubelet's \
        host machine and then exposed to the pod.
    :type fc: Optional[FCVolumeSource]
    :param flex_volume:FlexVolume represents a generic volume resource that is \
        provisioned/attached using an exec based plugin.
    :type flex_volume: Optional[FlexVolumeSource]
    :param flocker:Flocker represents a Flocker volume attached to a kubelet's host \
        machine. This depends on the Flocker control service being running
    :type flocker: Optional[FlockerVolumeSource]
    :param gce_persistent_disk:GCEPersistentDisk represents a GCE Disk resource that \
        is attached to a kubelet's host machine and then exposed to the pod. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type gce_persistent_disk: Optional[GCEPersistentDiskVolumeSource]
    :param glusterfs:Glusterfs represents a Glusterfs mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md
    :type glusterfs: Optional[GlusterfsVolumeSource]
    :param iscsi:ISCSI represents an ISCSI Disk resource that is attached to a \
        kubelet's host machine and then exposed to the pod. More info: \
        https://examples.k8s.io/volumes/iscsi/README.md
    :type iscsi: Optional[ISCSIVolumeSource]
    :param nfs:NFS represents an NFS mount on the host that shares a pod's lifetime \
        More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :type nfs: Optional[NFSVolumeSource]
    :param photon_persistent_disk:PhotonPersistentDisk represents a PhotonController \
        persistent disk attached and mounted on kubelets host machine
    :type photon_persistent_disk: Optional[PhotonPersistentDiskVolumeSource]
    :param portworx_volume:PortworxVolume represents a portworx volume attached and \
        mounted on kubelets host machine
    :type portworx_volume: Optional[PortworxVolumeSource]
    :param quobyte:Quobyte represents a Quobyte mount on the host that shares a pod's \
        lifetime
    :type quobyte: Optional[QuobyteVolumeSource]
    :param rbd:RBD represents a Rados Block Device mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md
    :type rbd: Optional[RBDVolumeSource]
    :param scale_io:ScaleIO represents a ScaleIO persistent volume attached and \
        mounted on Kubernetes nodes.
    :type scale_io: Optional[ScaleIOVolumeSource]
    :param storageos:StorageOS represents a StorageOS volume attached and mounted on \
        Kubernetes nodes.
    :type storageos: Optional[StorageOSVolumeSource]
    :param vsphere_volume:VsphereVolume represents a vSphere volume attached and \
        mounted on kubelets host machine
    :type vsphere_volume: Optional[VsphereVirtualDiskVolumeSource]
    """

    def __init__(
        self,
        name: str,
        config_map: ConfigMapVolumeSource,
        downward_api: DownwardAPIVolumeSource,
        empty_dir: EmptyDirVolumeSource,
        git_repo: GitRepoVolumeSource,
        host_path: HostPathVolumeSource,
        persistent_volume_claim: PersistentVolumeClaimVolumeSource,
        projected: ProjectedVolumeSource,
        secret: SecretVolumeSource,
        aws_elastic_block_store: Optional[AWSElasticBlockStoreVolumeSource] = None,
        azure_disk: Optional[AzureDiskVolumeSource] = None,
        azure_file: Optional[AzureFileVolumeSource] = None,
        cephfs: Optional[CephFSVolumeSource] = None,
        cinder: Optional[CinderVolumeSource] = None,
        csi: Optional[CSIVolumeSource] = None,
        fc: Optional[FCVolumeSource] = None,
        flex_volume: Optional[FlexVolumeSource] = None,
        flocker: Optional[FlockerVolumeSource] = None,
        gce_persistent_disk: Optional[GCEPersistentDiskVolumeSource] = None,
        glusterfs: Optional[GlusterfsVolumeSource] = None,
        iscsi: Optional[ISCSIVolumeSource] = None,
        nfs: Optional[NFSVolumeSource] = None,
        photon_persistent_disk: Optional[PhotonPersistentDiskVolumeSource] = None,
        portworx_volume: Optional[PortworxVolumeSource] = None,
        quobyte: Optional[QuobyteVolumeSource] = None,
        rbd: Optional[RBDVolumeSource] = None,
        scale_io: Optional[ScaleIOVolumeSource] = None,
        storageos: Optional[StorageOSVolumeSource] = None,
        vsphere_volume: Optional[VsphereVirtualDiskVolumeSource] = None,
    ):
        self.name = name
        self.configMap = config_map
        self.downwardAPI = downward_api
        self.emptyDir = empty_dir
        self.gitRepo = git_repo
        self.hostPath = host_path
        self.persistentVolumeClaim = persistent_volume_claim
        self.projected = projected
        self.secret = secret
        self.awsElasticBlockStore = aws_elastic_block_store
        self.azureDisk = azure_disk
        self.azureFile = azure_file
        self.cephfs = cephfs
        self.cinder = cinder
        self.csi = csi
        self.fc = fc
        self.flexVolume = flex_volume
        self.flocker = flocker
        self.gcePersistentDisk = gce_persistent_disk
        self.glusterfs = glusterfs
        self.iscsi = iscsi
        self.nfs = nfs
        self.photonPersistentDisk = photon_persistent_disk
        self.portworxVolume = portworx_volume
        self.quobyte = quobyte
        self.rbd = rbd
        self.scaleIO = scale_io
        self.storageos = storageos
        self.vsphereVolume = vsphere_volume


class Toleration(HelmYaml):
    """
    :param effect:Effect indicates the taint effect to match. Empty means match all \
        taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule \
        and NoExecute.
    :type effect: str
    :param key:Key is the taint key that the toleration applies to. Empty means match \
        all taint keys. If the key is empty, operator must be Exists; this combination \
        means to match all values and all keys.
    :type key: str
    :param toleration_seconds:TolerationSeconds represents the period of time the \
        toleration (which must be of effect NoExecute, otherwise this field is \
        ignored) tolerates the taint. By default, it is not set, which means tolerate \
        the taint forever (do not evict). Zero and negative values will be treated as \
        0 (evict immediately) by the system.
    :type toleration_seconds: int
    :param value:Value is the taint value the toleration matches to. If the operator \
        is Exists, the value should be empty, otherwise just a regular string.
    :type value: str
    :param operator:Operator represents a key's relationship to the value. Valid \
        operators are Exists and Equal. Defaults to Equal. Exists is equivalent to \
        wildcard for value, so that a pod can tolerate all taints of a particular \
        category.
    :type operator: Optional[str]
    """

    def __init__(
        self,
        effect: str,
        key: str,
        toleration_seconds: int,
        value: str,
        operator: Optional[str] = None,
    ):
        self.effect = effect
        self.key = key
        self.tolerationSeconds = toleration_seconds
        self.value = value
        self.operator = operator


class PodAffinityTerm(HelmYaml):
    """
    :param label_selector:A label query over a set of resources, in this case pods.
    :type label_selector: LabelSelector
    :param namespaces:namespaces specifies which namespaces the labelSelector applies \
        to (matches against); null or empty list means "this pod's namespace"
    :type namespaces: List[str]
    :param topology_key:This pod should be co-located (affinity) or not co-located \
        (anti-affinity) with the pods matching the labelSelector in the specified \
        namespaces, where co-located is defined as running on a node whose value of \
        the label with key topologyKey matches that of any node on which any of the \
        selected pods is running. Empty topologyKey is not allowed.
    :type topology_key: str
    """

    def __init__(
        self, label_selector: LabelSelector, namespaces: List[str], topology_key: str
    ):
        self.labelSelector = label_selector
        self.namespaces = namespaces
        self.topologyKey = topology_key


class WeightedPodAffinityTerm(HelmYaml):
    """
    :param pod_affinity_term:Required. A pod affinity term, associated with the \
        corresponding weight.
    :type pod_affinity_term: PodAffinityTerm
    :param weight:weight associated with matching the corresponding podAffinityTerm, \
        in the range 1-100.
    :type weight: int
    """

    def __init__(self, pod_affinity_term: PodAffinityTerm, weight: int):
        self.podAffinityTerm = pod_affinity_term
        self.weight = weight


class PodAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling affinity expressions, \
        etc.), compute a sum by iterating through the elements of this field and \
        adding "weight" to the sum if the node has pods which matches the \
        corresponding podAffinityTerm; the node(s) with the highest sum are the most \
        preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[WeightedPodAffinityTerm]
    :param required_during_scheduling_ignored_during_execution:If the affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the affinity requirements specified by \
        this field cease to be met at some point during pod execution (e.g. due to a \
        pod label update), the system may or may not try to eventually evict the pod \
        from its node. When there are multiple elements, the lists of nodes \
        corresponding to each podAffinityTerm are intersected, i.e. all terms must be \
        satisfied.
    :type required_during_scheduling_ignored_during_execution: List[PodAffinityTerm]
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            WeightedPodAffinityTerm
        ],
        required_during_scheduling_ignored_during_execution: List[PodAffinityTerm],
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class PodAntiAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the anti-affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling anti-affinity \
        expressions, etc.), compute a sum by iterating through the elements of this \
        field and adding "weight" to the sum if the node has pods which matches the \
        corresponding podAffinityTerm; the node(s) with the highest sum are the most \
        preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[WeightedPodAffinityTerm]
    :param required_during_scheduling_ignored_during_execution:If the anti-affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the anti-affinity requirements \
        specified by this field cease to be met at some point during pod execution \
        (e.g. due to a pod label update), the system may or may not try to eventually \
        evict the pod from its node. When there are multiple elements, the lists of \
        nodes corresponding to each podAffinityTerm are intersected, i.e. all terms \
        must be satisfied.
    :type required_during_scheduling_ignored_during_execution: List[PodAffinityTerm]
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            WeightedPodAffinityTerm
        ],
        required_during_scheduling_ignored_during_execution: List[PodAffinityTerm],
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class NodeSelectorRequirement(HelmYaml):
    """
    :param key:The label key that the selector applies to.
    :type key: str
    :param operator:Represents a key's relationship to a set of values. Valid \
        operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt.
    :type operator: str
    :param values:An array of string values. If the operator is In or NotIn, the \
        values array must be non-empty. If the operator is Exists or DoesNotExist, the \
        values array must be empty. If the operator is Gt or Lt, the values array must \
        have a single element, which will be interpreted as an integer. This array is \
        replaced during a strategic merge patch.
    :type values: List[str]
    """

    def __init__(self, key: str, operator: str, values: List[str]):
        self.key = key
        self.operator = operator
        self.values = values


class NodeSelectorTerm(HelmYaml):
    """
    :param match_fields:A list of node selector requirements by node's fields.
    :type match_fields: List[NodeSelectorRequirement]
    :param match_expressions:A list of node selector requirements by node's labels.
    :type match_expressions: Optional[List[NodeSelectorRequirement]]
    """

    def __init__(
        self,
        match_fields: List[NodeSelectorRequirement],
        match_expressions: Optional[List[NodeSelectorRequirement]] = None,
    ):
        self.matchFields = match_fields
        self.matchExpressions = match_expressions


class PreferredSchedulingTerm(HelmYaml):
    """
    :param preference:A node selector term, associated with the corresponding weight.
    :type preference: NodeSelectorTerm
    :param weight:Weight associated with matching the corresponding nodeSelectorTerm, \
        in the range 1-100.
    :type weight: int
    """

    def __init__(self, preference: NodeSelectorTerm, weight: int):
        self.preference = preference
        self.weight = weight


class NodeSelector(HelmYaml):
    """
    :param node_selector_terms:Required. A list of node selector terms. The terms are \
        ORed.
    :type node_selector_terms: List[NodeSelectorTerm]
    """

    def __init__(self, node_selector_terms: List[NodeSelectorTerm]):
        self.nodeSelectorTerms = node_selector_terms


class NodeAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling affinity expressions, \
        etc.), compute a sum by iterating through the elements of this field and \
        adding "weight" to the sum if the node matches the corresponding \
        matchExpressions; the node(s) with the highest sum are the most preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[PreferredSchedulingTerm]
    :param required_during_scheduling_ignored_during_execution:If the affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the affinity requirements specified by \
        this field cease to be met at some point during pod execution (e.g. due to an \
        update), the system may or may not try to eventually evict the pod from its \
        node.
    :type required_during_scheduling_ignored_during_execution: NodeSelector
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            PreferredSchedulingTerm
        ],
        required_during_scheduling_ignored_during_execution: NodeSelector,
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class Affinity(HelmYaml):
    """
    :param pod_affinity:Describes pod affinity scheduling rules (e.g. co-locate this \
        pod in the same node, zone, etc. as some other pod(s)).
    :type pod_affinity: PodAffinity
    :param pod_anti_affinity:Describes pod anti-affinity scheduling rules (e.g. avoid \
        putting this pod in the same node, zone, etc. as some other pod(s)).
    :type pod_anti_affinity: PodAntiAffinity
    :param node_affinity:Describes node affinity scheduling rules for the pod.
    :type node_affinity: Optional[NodeAffinity]
    """

    def __init__(
        self,
        pod_affinity: PodAffinity,
        pod_anti_affinity: PodAntiAffinity,
        node_affinity: Optional[NodeAffinity] = None,
    ):
        self.podAffinity = pod_affinity
        self.podAntiAffinity = pod_anti_affinity
        self.nodeAffinity = node_affinity


class PodReadinessGate(HelmYaml):
    """
    :param condition_type:ConditionType refers to a condition in the pod's condition \
        list with matching type.
    :type condition_type: str
    """

    def __init__(self, condition_type: str):
        self.conditionType = condition_type


class PodSpec(HelmYaml):
    """
    :param containers:List of containers belonging to the pod. Containers cannot \
        currently be added or removed. There must be at least one container in a Pod. \
        Cannot be updated.
    :type containers: List[Container]
    :param active_deadline_seconds:Optional duration in seconds the pod may be active \
        on the node relative to StartTime before the system will actively try to mark \
        it failed and kill associated containers. Value must be a positive integer.
    :type active_deadline_seconds: Optional[int]
    :param affinity:If specified, the pod's scheduling constraints
    :type affinity: Optional[Affinity]
    :param automount_service_account_token:AutomountServiceAccountToken indicates \
        whether a service account token should be automatically mounted.
    :type automount_service_account_token: Optional[bool]
    :param dns_config:Specifies the DNS parameters of a pod. Parameters specified here \
        will be merged to the generated DNS configuration based on DNSPolicy.
    :type dns_config: Optional[PodDNSConfig]
    :param dns_policy:Set DNS policy for the pod. Defaults to "ClusterFirst". Valid \
        values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS \
        parameters given in DNSConfig will be merged with the policy selected with \
        DNSPolicy. To have DNS options set along with hostNetwork, you have to specify \
        DNS policy explicitly to 'ClusterFirstWithHostNet'.
    :type dns_policy: Optional[str]
    :param enable_service_links:EnableServiceLinks indicates whether information about \
        services should be injected into pod's environment variables, matching the \
        syntax of Docker links. Optional: Defaults to true.
    :type enable_service_links: Optional[bool]
    :param ephemeral_containers:List of ephemeral containers run in this pod. \
        Ephemeral containers may be run in an existing pod to perform user-initiated \
        actions such as debugging. This list cannot be specified when creating a pod, \
        and it cannot be modified by updating the pod spec. In order to add an \
        ephemeral container to an existing pod, use the pod's ephemeralcontainers \
        subresource. This field is alpha-level and is only honored by servers that \
        enable the EphemeralContainers feature.
    :type ephemeral_containers: Optional[List[EphemeralContainer]]
    :param host_aliases:HostAliases is an optional list of hosts and IPs that will be \
        injected into the pod's hosts file if specified. This is only valid for \
        non-hostNetwork pods.
    :type host_aliases: Optional[List[HostAlias]]
    :param host_ipc:Use the host's ipc namespace. Optional: Default to false.
    :type host_ipc: Optional[bool]
    :param host_network:Host networking requested for this pod. Use the host's network \
        namespace. If this option is set, the ports that will be used must be \
        specified. Default to false.
    :type host_network: Optional[bool]
    :param host_pid:Use the host's pid namespace. Optional: Default to false.
    :type host_pid: Optional[bool]
    :param hostname:Specifies the hostname of the Pod If not specified, the pod's \
        hostname will be set to a system-defined value.
    :type hostname: Optional[str]
    :param image_pull_secrets:ImagePullSecrets is an optional list of references to \
        secrets in the same namespace to use for pulling any of the images used by \
        this PodSpec. If specified, these secrets will be passed to individual puller \
        implementations for them to use. For example, in the case of docker, only \
        DockerConfig type secrets are honored. More info: \
        https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod  # noqa
    :type image_pull_secrets: Optional[List[LocalObjectReference]]
    :param init_containers:List of initialization containers belonging to the pod. \
        Init containers are executed in order prior to containers being started. If \
        any init container fails, the pod is considered to have failed and is handled \
        according to its restartPolicy. The name for an init container or normal \
        container must be unique among all containers. Init containers may not have \
        Lifecycle actions, Readiness probes, Liveness probes, or Startup probes. The \
        resourceRequirements of an init container are taken into account during \
        scheduling by finding the highest request/limit for each resource type, and \
        then using the max of of that value or the sum of the normal containers. \
        Limits are applied to init containers in a similar fashion. Init containers \
        cannot currently be added or removed. Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
    :type init_containers: Optional[List[Container]]
    :param node_name:NodeName is a request to schedule this pod onto a specific node. \
        If it is non-empty, the scheduler simply schedules this pod onto that node, \
        assuming that it fits resource requirements.
    :type node_name: Optional[str]
    :param node_selector:NodeSelector is a selector which must be true for the pod to \
        fit on a node. Selector which must match a node's labels for the pod to be \
        scheduled on that node. More info: \
        https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
    :type node_selector: Optional[dict]
    :param overhead:Overhead represents the resource overhead associated with running \
        a pod for a given RuntimeClass. This field will be autopopulated at admission \
        time by the RuntimeClass admission controller. If the RuntimeClass admission \
        controller is enabled, overhead must not be set in Pod create requests. The \
        RuntimeClass admission controller will reject Pod create requests which have \
        the overhead already set. If RuntimeClass is configured and selected in the \
        PodSpec, Overhead will be set to the value defined in the corresponding \
        RuntimeClass, otherwise it will remain unset and treated as zero. More info: \
        https://git.k8s.io/enhancements/keps/sig-node/20190226-pod-overhead.md This \
        field is alpha-level as of Kubernetes v1.16, and is only honored by servers \
        that enable the PodOverhead feature.
    :type overhead: Optional[dict]
    :param preemption_policy:PreemptionPolicy is the Policy for preempting pods with \
        lower priority. One of Never, PreemptLowerPriority. Defaults to \
        PreemptLowerPriority if unset. This field is alpha-level and is only honored \
        by servers that enable the NonPreemptingPriority feature.
    :type preemption_policy: Optional[str]
    :param priority:The priority value. Various system components use this field to \
        find the priority of the pod. When Priority Admission Controller is enabled, \
        it prevents users from setting this field. The admission controller populates \
        this field from PriorityClassName. The higher the value, the higher the \
        priority.
    :type priority: Optional[int]
    :param priority_class_name:If specified, indicates the pod's priority. \
        "system-node-critical" and "system-cluster-critical" are two special keywords \
        which indicate the highest priorities with the former being the highest \
        priority. Any other name must be defined by creating a PriorityClass object \
        with that name. If not specified, the pod priority will be default or zero if \
        there is no default.
    :type priority_class_name: Optional[str]
    :param readiness_gates:If specified, all readiness gates will be evaluated for pod \
        readiness. A pod is ready when all its containers are ready AND all conditions \
        specified in the readiness gates have status equal to "True" More info: \
        https://git.k8s.io/enhancements/keps/sig-network/0007-pod-ready%2B%2B.md
    :type readiness_gates: Optional[List[PodReadinessGate]]
    :param restart_policy:Restart policy for all containers within the pod. One of \
        Always, OnFailure, Never. Default to Always. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy  # noqa
    :type restart_policy: Optional[str]
    :param runtime_class_name:RuntimeClassName refers to a RuntimeClass object in the \
        node.k8s.io group, which should be used to run this pod.  If no RuntimeClass \
        resource matches the named class, the pod will not be run. If unset or empty, \
        the "legacy" RuntimeClass will be used, which is an implicit class with an \
        empty definition that uses the default runtime handler. More info: \
        https://git.k8s.io/enhancements/keps/sig-node/runtime-class.md This is a beta \
        feature as of Kubernetes v1.14.
    :type runtime_class_name: Optional[str]
    :param scheduler_name:If specified, the pod will be dispatched by specified \
        scheduler. If not specified, the pod will be dispatched by default scheduler.
    :type scheduler_name: Optional[str]
    :param security_context:SecurityContext holds pod-level security attributes and \
        common container settings. Optional: Defaults to empty.  See type description \
        for default values of each field.
    :type security_context: Optional[PodSecurityContext]
    :param service_account:DeprecatedServiceAccount is a depreciated alias for \
        ServiceAccountName. Deprecated: Use serviceAccountName instead.
    :type service_account: Optional[str]
    :param service_account_name:ServiceAccountName is the name of the ServiceAccount \
        to use to run this pod. More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/  # noqa
    :type service_account_name: Optional[str]
    :param share_process_namespace:Share a single process namespace between all of the \
        containers in a pod. When this is set containers will be able to view and \
        signal processes from other containers in the same pod, and the first process \
        in each container will not be assigned PID 1. HostPID and \
        ShareProcessNamespace cannot both be set. Optional: Default to false.
    :type share_process_namespace: Optional[bool]
    :param subdomain:If specified, the fully qualified Pod hostname will be \
        "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not \
        specified, the pod will not have a domainname at all.
    :type subdomain: Optional[str]
    :param termination_grace_period_seconds:Optional duration in seconds the pod needs \
        to terminate gracefully. May be decreased in delete request. Value must be \
        non-negative integer. The value zero indicates delete immediately. If this \
        value is nil, the default grace period will be used instead. The grace period \
        is the duration in seconds after the processes running in the pod are sent a \
        termination signal and the time when the processes are forcibly halted with a \
        kill signal. Set this value longer than the expected cleanup time for your \
        process. Defaults to 30 seconds.
    :type termination_grace_period_seconds: Optional[int]
    :param tolerations:If specified, the pod's tolerations.
    :type tolerations: Optional[List[Toleration]]
    :param topology_spread_constraints:TopologySpreadConstraints describes how a group \
        of pods ought to spread across topology domains. Scheduler will schedule pods \
        in a way which abides by the constraints. This field is only honored by \
        clusters that enable the EvenPodsSpread feature. All topologySpreadConstraints \
        are ANDed.
    :type topology_spread_constraints: Optional[List[TopologySpreadConstraint]]
    :param volumes:List of volumes that can be mounted by containers belonging to the \
        pod. More info: https://kubernetes.io/docs/concepts/storage/volumes
    :type volumes: Optional[List[Volume]]
    """

    def __init__(
        self,
        containers: List[Container],
        active_deadline_seconds: Optional[int] = None,
        affinity: Optional[Affinity] = None,
        automount_service_account_token: Optional[bool] = None,
        dns_config: Optional[PodDNSConfig] = None,
        dns_policy: Optional[str] = None,
        enable_service_links: Optional[bool] = None,
        ephemeral_containers: Optional[List[EphemeralContainer]] = None,
        host_aliases: Optional[List[HostAlias]] = None,
        host_ipc: Optional[bool] = None,
        host_network: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        hostname: Optional[str] = None,
        image_pull_secrets: Optional[List[LocalObjectReference]] = None,
        init_containers: Optional[List[Container]] = None,
        node_name: Optional[str] = None,
        node_selector: Optional[dict] = None,
        overhead: Optional[dict] = None,
        preemption_policy: Optional[str] = None,
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = None,
        readiness_gates: Optional[List[PodReadinessGate]] = None,
        restart_policy: Optional[str] = None,
        runtime_class_name: Optional[str] = None,
        scheduler_name: Optional[str] = None,
        security_context: Optional[PodSecurityContext] = None,
        service_account: Optional[str] = None,
        service_account_name: Optional[str] = None,
        share_process_namespace: Optional[bool] = None,
        subdomain: Optional[str] = None,
        termination_grace_period_seconds: Optional[int] = None,
        tolerations: Optional[List[Toleration]] = None,
        topology_spread_constraints: Optional[List[TopologySpreadConstraint]] = None,
        volumes: Optional[List[Volume]] = None,
    ):
        self.containers = containers
        self.activeDeadlineSeconds = active_deadline_seconds
        self.affinity = affinity
        self.automountServiceAccountToken = automount_service_account_token
        self.dnsConfig = dns_config
        self.dnsPolicy = dns_policy
        self.enableServiceLinks = enable_service_links
        self.ephemeralContainers = ephemeral_containers
        self.hostAliases = host_aliases
        self.hostIPC = host_ipc
        self.hostNetwork = host_network
        self.hostPID = host_pid
        self.hostname = hostname
        self.imagePullSecrets = image_pull_secrets
        self.initContainers = init_containers
        self.nodeName = node_name
        self.nodeSelector = node_selector
        self.overhead = overhead
        self.preemptionPolicy = preemption_policy
        self.priority = priority
        self.priorityClassName = priority_class_name
        self.readinessGates = readiness_gates
        self.restartPolicy = restart_policy
        self.runtimeClassName = runtime_class_name
        self.schedulerName = scheduler_name
        self.securityContext = security_context
        self.serviceAccount = service_account
        self.serviceAccountName = service_account_name
        self.shareProcessNamespace = share_process_namespace
        self.subdomain = subdomain
        self.terminationGracePeriodSeconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topologySpreadConstraints = topology_spread_constraints
        self.volumes = volumes


class PodTemplateSpec(HelmYaml):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the pod. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: PodSpec
    """

    def __init__(self, metadata: ObjectMeta, spec: PodSpec):
        self.metadata = metadata
        self.spec = spec


class PodTemplate(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param template:Template defines the pods that will be created from this pod \
        template. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type template: PodTemplateSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        template: PodTemplateSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.template = template


class SecretReference(HelmYaml):
    """
    :param name:Name is unique within a namespace to reference a secret resource.
    :type name: str
    :param namespace:Namespace defines the space within which the secret name must be \
        unique.
    :type namespace: Optional[str]
    """

    def __init__(self, name: str, namespace: Optional[str] = None):
        self.name = name
        self.namespace = namespace


class CSIPersistentVolumeSource(HelmYaml):
    """
    :param driver:Driver is the name of the driver to use for this volume. Required.
    :type driver: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs".
    :type fs_type: str
    :param volume_attributes:Attributes of the volume to publish.
    :type volume_attributes: dict
    :param volume_handle:VolumeHandle is the unique volume name returned by the CSI \
        volume plugin’s CreateVolume to refer to the volume on all subsequent calls. \
        Required.
    :type volume_handle: str
    :param controller_expand_secret_ref:ControllerExpandSecretRef is a reference to \
        the secret object containing sensitive information to pass to the CSI driver \
        to complete the CSI ControllerExpandVolume call. This is an alpha field and \
        requires enabling ExpandCSIVolumes feature gate. This field is optional, and \
        may be empty if no secret is required. If the secret object contains more than \
        one secret, all secrets are passed.
    :type controller_expand_secret_ref: Optional[SecretReference]
    :param controller_publish_secret_ref:ControllerPublishSecretRef is a reference to \
        the secret object containing sensitive information to pass to the CSI driver \
        to complete the CSI ControllerPublishVolume and ControllerUnpublishVolume \
        calls. This field is optional, and may be empty if no secret is required. If \
        the secret object contains more than one secret, all secrets are passed.
    :type controller_publish_secret_ref: Optional[SecretReference]
    :param node_publish_secret_ref:NodePublishSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodePublishVolume and NodeUnpublishVolume calls. This field is \
        optional, and may be empty if no secret is required. If the secret object \
        contains more than one secret, all secrets are passed.
    :type node_publish_secret_ref: Optional[SecretReference]
    :param node_stage_secret_ref:NodeStageSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodeStageVolume and NodeStageVolume and NodeUnstageVolume calls. This \
        field is optional, and may be empty if no secret is required. If the secret \
        object contains more than one secret, all secrets are passed.
    :type node_stage_secret_ref: Optional[SecretReference]
    :param read_only:Optional: The value to pass to ControllerPublishVolumeRequest. \
        Defaults to false (read/write).
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        volume_attributes: dict,
        volume_handle: str,
        controller_expand_secret_ref: Optional[SecretReference] = None,
        controller_publish_secret_ref: Optional[SecretReference] = None,
        node_publish_secret_ref: Optional[SecretReference] = None,
        node_stage_secret_ref: Optional[SecretReference] = None,
        read_only: Optional[bool] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.volumeAttributes = volume_attributes
        self.volumeHandle = volume_handle
        self.controllerExpandSecretRef = controller_expand_secret_ref
        self.controllerPublishSecretRef = controller_publish_secret_ref
        self.nodePublishSecretRef = node_publish_secret_ref
        self.nodeStageSecretRef = node_stage_secret_ref
        self.readOnly = read_only


class StorageOSPersistentVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :type fs_type: str
    :param volume_name:VolumeName is the human-readable name of the StorageOS volume.  \
        Volume names are only unique within a namespace.
    :type volume_name: str
    :param volume_namespace:VolumeNamespace specifies the scope of the volume within \
        StorageOS.  If no namespace is specified then the Pod's namespace will be \
        used.  This allows the Kubernetes name scoping to be mirrored within StorageOS \
        for tighter integration. Set VolumeName to any name to override the default \
        behaviour. Set to "default" if you are not using namespaces within StorageOS. \
        Namespaces that do not pre-exist within StorageOS will be created.
    :type volume_namespace: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef specifies the secret to use for obtaining the \
        StorageOS API credentials.  If not specified, default values will be \
        attempted.
    :type secret_ref: Optional[ObjectReference]
    """

    def __init__(
        self,
        fs_type: str,
        volume_name: str,
        volume_namespace: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[ObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeName = volume_name
        self.volumeNamespace = volume_namespace
        self.readOnly = read_only
        self.secretRef = secret_ref


class TopologySelectorLabelRequirement(HelmYaml):
    """
    :param key:The label key that the selector applies to.
    :type key: str
    :param values:An array of string values. One value must match the label to be \
        selected. Each entry in Values is ORed.
    :type values: List[str]
    """

    def __init__(self, key: str, values: List[str]):
        self.key = key
        self.values = values


class TopologySelectorTerm(HelmYaml):
    """
    :param match_label_expressions:A list of topology selector requirements by labels.
    :type match_label_expressions: List[TopologySelectorLabelRequirement]
    """

    def __init__(self, match_label_expressions: List[TopologySelectorLabelRequirement]):
        self.matchLabelExpressions = match_label_expressions


class ServiceAccount(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param automount_service_account_token:AutomountServiceAccountToken indicates \
        whether pods running as this service account should have an API token \
        automatically mounted. Can be overridden at the pod level.
    :type automount_service_account_token: Optional[bool]
    :param image_pull_secrets:ImagePullSecrets is a list of references to secrets in \
        the same namespace to use for pulling any images in pods that reference this \
        ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can \
        be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. \
        More info: \
        https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod  # noqa
    :type image_pull_secrets: Optional[List[LocalObjectReference]]
    :param secrets:Secrets is the list of secrets allowed to be used by pods running \
        using this ServiceAccount. More info: \
        https://kubernetes.io/docs/concepts/configuration/secret
    :type secrets: Optional[List[ObjectReference]]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        automount_service_account_token: Optional[bool] = None,
        image_pull_secrets: Optional[List[LocalObjectReference]] = None,
        secrets: Optional[List[ObjectReference]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.automountServiceAccountToken = automount_service_account_token
        self.imagePullSecrets = image_pull_secrets
        self.secrets = secrets


class ComponentCondition(HelmYaml):
    """
    :param error:Condition error code for a component. For example, a health check \
        error code.
    :type error: str
    :param message:Message about the condition for a component. For example, \
        information about a health check.
    :type message: str
    :param type:Type of condition for a component. Valid value: "Healthy"
    :type type: str
    """

    def __init__(self, error: str, message: str, type: str):
        self.error = error
        self.message = message
        self.type = type


class TypedLocalObjectReference(KubernetesBaseObject):
    """
    :param name:Name is the name of resource being referenced
    :type name: str
    :param api_group:APIGroup is the group for the resource being referenced. If \
        APIGroup is not specified, the specified Kind must be in the core API group. \
        For any other third-party types, APIGroup is required.
    :type api_group: Optional[str]
    """

    def __init__(self, name: str, api_group: Optional[str] = None):
        self.name = name
        self.apiGroup = api_group


class PersistentVolumeClaimSpec(HelmYaml):
    """
    :param access_modes:AccessModes contains the desired access modes the volume \
        should have. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1
    :type access_modes: List[str]
    :param resources:Resources represents the minimum resources the volume should \
        have. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources
    :type resources: ResourceRequirements
    :param data_source:This field can be used to specify either: * An existing \
        VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot - Beta) * An \
        existing PVC (PersistentVolumeClaim) * An existing custom resource/object that \
        implements data population (Alpha) In order to use VolumeSnapshot object \
        types, the appropriate feature gate must be enabled (VolumeSnapshotDataSource \
        or AnyVolumeDataSource) If the provisioner or an external controller can \
        support the specified data source, it will create a new volume based on the \
        contents of the specified data source. If the specified data source is not \
        supported, the volume will not be created and the failure will be reported as \
        an event. In the future, we plan to support more data source types and the \
        behavior of the provisioner may change.
    :type data_source: Optional[TypedLocalObjectReference]
    :param selector:A label query over volumes to consider for binding.
    :type selector: Optional[LabelSelector]
    :param storage_class_name:Name of the StorageClass required by the claim. More \
        info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1
    :type storage_class_name: Optional[str]
    :param volume_mode:volumeMode defines what type of volume is required by the \
        claim. Value of Filesystem is implied when not included in claim spec.
    :type volume_mode: Optional[str]
    :param volume_name:VolumeName is the binding reference to the PersistentVolume \
        backing this claim.
    :type volume_name: Optional[str]
    """

    def __init__(
        self,
        access_modes: List[str],
        resources: ResourceRequirements,
        data_source: Optional[TypedLocalObjectReference] = None,
        selector: Optional[LabelSelector] = None,
        storage_class_name: Optional[str] = None,
        volume_mode: Optional[str] = None,
        volume_name: Optional[str] = None,
    ):
        self.accessModes = access_modes
        self.resources = resources
        self.dataSource = data_source
        self.selector = selector
        self.storageClassName = storage_class_name
        self.volumeMode = volume_mode
        self.volumeName = volume_name


class PersistentVolumeClaimCondition(HelmYaml):
    """
    :param last_probe_time:Last time we probed the condition.
    :type last_probe_time: time
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:Human-readable message indicating details about last transition.
    :type message: str
    :param reason:Unique, this should be a short, machine understandable string that \
        gives the reason for condition's last transition. If it reports \
        "ResizeStarted" that means the underlying persistent volume is being resized.
    :type reason: str
    :param type:None
    :type type: str
    """

    def __init__(
        self,
        last_probe_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastProbeTime = last_probe_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class PersistentVolumeClaim(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the desired characteristics of a volume requested by a \
        pod author. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :type spec: PersistentVolumeClaimSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PersistentVolumeClaimSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class FlexPersistentVolumeSource(HelmYaml):
    """
    :param driver:Driver is the name of the driver to use for this volume.
    :type driver: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem \
        depends on FlexVolume script.
    :type fs_type: str
    :param options:Optional: Extra command options if any.
    :type options: Optional[dict]
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:Optional: SecretRef is reference to the secret object containing \
        sensitive information to pass to the plugin scripts. This may be empty if no \
        secret object is specified. If the secret object contains more than one \
        secret, all secrets are passed to the plugin scripts.
    :type secret_ref: Optional[SecretReference]
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        options: Optional[dict] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.options = options
        self.readOnly = read_only
        self.secretRef = secret_ref


class CinderPersistentVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly \
        inferred to be "ext4" if unspecified. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type fs_type: str
    :param volume_id:volume id used to identify the volume in cinder. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type volume_id: str
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :type read_only: Optional[bool]
    :param secret_ref:Optional: points to a secret object containing parameters used \
        to connect to OpenStack.
    :type secret_ref: Optional[SecretReference]
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only
        self.secretRef = secret_ref


class RBDPersistentVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#rbd
    :type fs_type: str
    :param image:The rados image name. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type image: str
    :param monitors:A collection of Ceph monitors. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type monitors: List[str]
    :param keyring:Keyring is the path to key ring for RBDUser. Default is \
        /etc/ceph/keyring. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type keyring: Optional[str]
    :param pool:The rados pool name. Default is rbd. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type pool: Optional[str]
    :param read_only:ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef is name of the authentication secret for RBDUser. If \
        provided overrides keyring. Default is nil. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type secret_ref: Optional[SecretReference]
    :param user:The rados user name. Default is admin. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :type user: Optional[str]
    """

    def __init__(
        self,
        fs_type: str,
        image: str,
        monitors: List[str],
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
        user: Optional[str] = None,
    ):
        self.fsType = fs_type
        self.image = image
        self.monitors = monitors
        self.keyring = keyring
        self.pool = pool
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.user = user


class ScaleIOPersistentVolumeSource(HelmYaml):
    """
    :param gateway:The host address of the ScaleIO API Gateway.
    :type gateway: str
    :param protection_domain:The name of the ScaleIO Protection Domain for the \
        configured storage.
    :type protection_domain: str
    :param ssl_enabled:Flag to enable/disable SSL communication with Gateway, default \
        false
    :type ssl_enabled: bool
    :param storage_pool:The ScaleIO Storage Pool associated with the protection \
        domain.
    :type storage_pool: str
    :param system:The name of the storage system as configured in ScaleIO.
    :type system: str
    :param volume_name:The name of a volume already created in the ScaleIO system that \
        is associated with this volume source.
    :type volume_name: str
    :param fs_type:Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Default is "xfs"
    :type fs_type: Optional[str]
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_ref:SecretRef references to the secret for ScaleIO user and other \
        sensitive information. If this is not provided, Login operation will fail.
    :type secret_ref: Optional[SecretReference]
    :param storage_mode:Indicates whether the storage for a volume should be \
        ThickProvisioned or ThinProvisioned. Default is ThinProvisioned.
    :type storage_mode: Optional[str]
    """

    def __init__(
        self,
        gateway: str,
        protection_domain: str,
        ssl_enabled: bool,
        storage_pool: str,
        system: str,
        volume_name: str,
        fs_type: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
        storage_mode: Optional[str] = None,
    ):
        self.gateway = gateway
        self.protectionDomain = protection_domain
        self.sslEnabled = ssl_enabled
        self.storagePool = storage_pool
        self.system = system
        self.volumeName = volume_name
        self.fsType = fs_type
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.storageMode = storage_mode


class CephFSPersistentVolumeSource(HelmYaml):
    """
    :param monitors:Required: Monitors is a collection of Ceph monitors More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type monitors: List[str]
    :param path:Optional: Used as the mounted root, rather than the full Ceph tree, \
        default is /
    :type path: Optional[str]
    :param read_only:Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type read_only: Optional[bool]
    :param secret_file:Optional: SecretFile is the path to key ring for User, default \
        is /etc/ceph/user.secret More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type secret_file: Optional[str]
    :param secret_ref:Optional: SecretRef is reference to the authentication secret \
        for User, default is empty. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type secret_ref: Optional[SecretReference]
    :param user:Optional: User is the rados user name, default is admin More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :type user: Optional[str]
    """

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_file: Optional[str] = None,
        secret_ref: Optional[SecretReference] = None,
        user: Optional[str] = None,
    ):
        self.monitors = monitors
        self.path = path
        self.readOnly = read_only
        self.secretFile = secret_file
        self.secretRef = secret_ref
        self.user = user


class ISCSIPersistentVolumeSource(HelmYaml):
    """
    :param chap_auth_discovery:whether support iSCSI Discovery CHAP authentication
    :type chap_auth_discovery: bool
    :param chap_auth_session:whether support iSCSI Session CHAP authentication
    :type chap_auth_session: bool
    :param fs_type:Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi
    :type fs_type: str
    :param initiator_name:Custom iSCSI Initiator Name. If initiatorName is specified \
        with iscsiInterface simultaneously, new iSCSI interface <target \
        portal>:<volume name> will be created for the connection.
    :type initiator_name: str
    :param iqn:Target iSCSI Qualified Name.
    :type iqn: str
    :param lun:iSCSI Target Lun number.
    :type lun: int
    :param portals:iSCSI Target Portal List. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :type portals: List[str]
    :param secret_ref:CHAP Secret for iSCSI target and initiator authentication
    :type secret_ref: SecretReference
    :param target_portal:iSCSI Target Portal. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :type target_portal: str
    :param iscsi_interface:iSCSI Interface Name that uses an iSCSI transport. Defaults \
        to 'default' (tcp).
    :type iscsi_interface: Optional[str]
    :param read_only:ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false.
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        chap_auth_discovery: bool,
        chap_auth_session: bool,
        fs_type: str,
        initiator_name: str,
        iqn: str,
        lun: int,
        portals: List[str],
        secret_ref: SecretReference,
        target_portal: str,
        iscsi_interface: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.chapAuthDiscovery = chap_auth_discovery
        self.chapAuthSession = chap_auth_session
        self.fsType = fs_type
        self.initiatorName = initiator_name
        self.iqn = iqn
        self.lun = lun
        self.portals = portals
        self.secretRef = secret_ref
        self.targetPortal = target_portal
        self.iscsiInterface = iscsi_interface
        self.readOnly = read_only


class GlusterfsPersistentVolumeSource(HelmYaml):
    """
    :param endpoints:EndpointsName is the endpoint name that details Glusterfs \
        topology. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type endpoints: str
    :param path:Path is the Glusterfs volume path. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type path: str
    :param endpoints_namespace:EndpointsNamespace is the namespace that contains \
        Glusterfs endpoint. If this field is empty, the EndpointNamespace defaults to \
        the same namespace as the bound PVC. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type endpoints_namespace: Optional[str]
    :param read_only:ReadOnly here will force the Glusterfs volume to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :type read_only: Optional[bool]
    """

    def __init__(
        self,
        endpoints: str,
        path: str,
        endpoints_namespace: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.endpoints = endpoints
        self.path = path
        self.endpointsNamespace = endpoints_namespace
        self.readOnly = read_only


class LocalVolumeSource(HelmYaml):
    """
    :param fs_type:Filesystem type to mount. It applies only when the Path is a block \
        device. Must be a filesystem type supported by the host operating system. Ex. \
        "ext4", "xfs", "ntfs". The default value is to auto-select a fileystem if \
        unspecified.
    :type fs_type: str
    :param path:The full path to the volume on the node. It can be either a directory \
        or block device (disk, partition, ...).
    :type path: str
    """

    def __init__(self, fs_type: str, path: str):
        self.fsType = fs_type
        self.path = path


class AzureFilePersistentVolumeSource(HelmYaml):
    """
    :param secret_name:the name of secret that contains Azure Storage Account Name and \
        Key
    :type secret_name: str
    :param share_name:Share Name
    :type share_name: str
    :param read_only:Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :type read_only: Optional[bool]
    :param secret_namespace:the namespace of the secret that contains Azure Storage \
        Account Name and Key default is the same as the Pod
    :type secret_namespace: Optional[str]
    """

    def __init__(
        self,
        secret_name: str,
        share_name: str,
        read_only: Optional[bool] = None,
        secret_namespace: Optional[str] = None,
    ):
        self.secretName = secret_name
        self.shareName = share_name
        self.readOnly = read_only
        self.secretNamespace = secret_namespace


class VolumeNodeAffinity(HelmYaml):
    """
    :param required:Required specifies hard node constraints that must be met.
    :type required: NodeSelector
    """

    def __init__(self, required: NodeSelector):
        self.required = required


class PersistentVolumeSpec(HelmYaml):
    """
    :param access_modes:AccessModes contains all ways the volume can be mounted. More \
        info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes
    :type access_modes: List[str]
    :param capacity:A description of the persistent volume's resources and capacity. \
        More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#capacity
    :type capacity: dict
    :param host_path:HostPath represents a directory on the host. Provisioned by a \
        developer or tester. This is useful for single-node development and testing \
        only! On-host storage is not supported in any way and WILL NOT WORK in a \
        multi-node cluster. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :type host_path: HostPathVolumeSource
    :param aws_elastic_block_store:AWSElasticBlockStore represents an AWS Disk \
        resource that is attached to a kubelet's host machine and then exposed to the \
        pod. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :type aws_elastic_block_store: Optional[AWSElasticBlockStoreVolumeSource]
    :param azure_disk:AzureDisk represents an Azure Data Disk mount on the host and \
        bind mount to the pod.
    :type azure_disk: Optional[AzureDiskVolumeSource]
    :param azure_file:AzureFile represents an Azure File Service mount on the host and \
        bind mount to the pod.
    :type azure_file: Optional[AzureFilePersistentVolumeSource]
    :param cephfs:CephFS represents a Ceph FS mount on the host that shares a pod's \
        lifetime
    :type cephfs: Optional[CephFSPersistentVolumeSource]
    :param cinder:Cinder represents a cinder volume attached and mounted on kubelets \
        host machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md
    :type cinder: Optional[CinderPersistentVolumeSource]
    :param claim_ref:ClaimRef is part of a bi-directional binding between \
        PersistentVolume and PersistentVolumeClaim. Expected to be non-nil when bound. \
        claim.VolumeName is the authoritative bind between PV and PVC. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#binding
    :type claim_ref: Optional[ObjectReference]
    :param csi:CSI represents storage that is handled by an external CSI driver (Beta \
        feature).
    :type csi: Optional[CSIPersistentVolumeSource]
    :param fc:FC represents a Fibre Channel resource that is attached to a kubelet's \
        host machine and then exposed to the pod.
    :type fc: Optional[FCVolumeSource]
    :param flex_volume:FlexVolume represents a generic volume resource that is \
        provisioned/attached using an exec based plugin.
    :type flex_volume: Optional[FlexPersistentVolumeSource]
    :param flocker:Flocker represents a Flocker volume attached to a kubelet's host \
        machine and exposed to the pod for its usage. This depends on the Flocker \
        control service being running
    :type flocker: Optional[FlockerVolumeSource]
    :param gce_persistent_disk:GCEPersistentDisk represents a GCE Disk resource that \
        is attached to a kubelet's host machine and then exposed to the pod. \
        Provisioned by an admin. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :type gce_persistent_disk: Optional[GCEPersistentDiskVolumeSource]
    :param glusterfs:Glusterfs represents a Glusterfs volume that is attached to a \
        host and exposed to the pod. Provisioned by an admin. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md
    :type glusterfs: Optional[GlusterfsPersistentVolumeSource]
    :param iscsi:ISCSI represents an ISCSI Disk resource that is attached to a \
        kubelet's host machine and then exposed to the pod. Provisioned by an admin.
    :type iscsi: Optional[ISCSIPersistentVolumeSource]
    :param local:Local represents directly-attached storage with node affinity
    :type local: Optional[LocalVolumeSource]
    :param mount_options:A list of mount options, e.g. ["ro", "soft"]. Not validated - \
        mount will simply fail if one is invalid. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes/#mount-options
    :type mount_options: Optional[List[str]]
    :param nfs:NFS represents an NFS mount on the host. Provisioned by an admin. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :type nfs: Optional[NFSVolumeSource]
    :param node_affinity:NodeAffinity defines constraints that limit what nodes this \
        volume can be accessed from. This field influences the scheduling of pods that \
        use this volume.
    :type node_affinity: Optional[VolumeNodeAffinity]
    :param persistent_volume_reclaim_policy:What happens to a persistent volume when \
        released from its claim. Valid options are Retain (default for manually \
        created PersistentVolumes), Delete (default for dynamically provisioned \
        PersistentVolumes), and Recycle (deprecated). Recycle must be supported by the \
        volume plugin underlying this PersistentVolume. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#reclaiming
    :type persistent_volume_reclaim_policy: Optional[str]
    :param photon_persistent_disk:PhotonPersistentDisk represents a PhotonController \
        persistent disk attached and mounted on kubelets host machine
    :type photon_persistent_disk: Optional[PhotonPersistentDiskVolumeSource]
    :param portworx_volume:PortworxVolume represents a portworx volume attached and \
        mounted on kubelets host machine
    :type portworx_volume: Optional[PortworxVolumeSource]
    :param quobyte:Quobyte represents a Quobyte mount on the host that shares a pod's \
        lifetime
    :type quobyte: Optional[QuobyteVolumeSource]
    :param rbd:RBD represents a Rados Block Device mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md
    :type rbd: Optional[RBDPersistentVolumeSource]
    :param scale_io:ScaleIO represents a ScaleIO persistent volume attached and \
        mounted on Kubernetes nodes.
    :type scale_io: Optional[ScaleIOPersistentVolumeSource]
    :param storage_class_name:Name of StorageClass to which this persistent volume \
        belongs. Empty value means that this volume does not belong to any \
        StorageClass.
    :type storage_class_name: Optional[str]
    :param storageos:StorageOS represents a StorageOS volume that is attached to the \
        kubelet's host machine and mounted into the pod More info: \
        https://examples.k8s.io/volumes/storageos/README.md
    :type storageos: Optional[StorageOSPersistentVolumeSource]
    :param volume_mode:volumeMode defines if a volume is intended to be used with a \
        formatted filesystem or to remain in raw block state. Value of Filesystem is \
        implied when not included in spec.
    :type volume_mode: Optional[str]
    :param vsphere_volume:VsphereVolume represents a vSphere volume attached and \
        mounted on kubelets host machine
    :type vsphere_volume: Optional[VsphereVirtualDiskVolumeSource]
    """

    def __init__(
        self,
        access_modes: List[str],
        capacity: dict,
        host_path: HostPathVolumeSource,
        aws_elastic_block_store: Optional[AWSElasticBlockStoreVolumeSource] = None,
        azure_disk: Optional[AzureDiskVolumeSource] = None,
        azure_file: Optional[AzureFilePersistentVolumeSource] = None,
        cephfs: Optional[CephFSPersistentVolumeSource] = None,
        cinder: Optional[CinderPersistentVolumeSource] = None,
        claim_ref: Optional[ObjectReference] = None,
        csi: Optional[CSIPersistentVolumeSource] = None,
        fc: Optional[FCVolumeSource] = None,
        flex_volume: Optional[FlexPersistentVolumeSource] = None,
        flocker: Optional[FlockerVolumeSource] = None,
        gce_persistent_disk: Optional[GCEPersistentDiskVolumeSource] = None,
        glusterfs: Optional[GlusterfsPersistentVolumeSource] = None,
        iscsi: Optional[ISCSIPersistentVolumeSource] = None,
        local: Optional[LocalVolumeSource] = None,
        mount_options: Optional[List[str]] = None,
        nfs: Optional[NFSVolumeSource] = None,
        node_affinity: Optional[VolumeNodeAffinity] = None,
        persistent_volume_reclaim_policy: Optional[str] = None,
        photon_persistent_disk: Optional[PhotonPersistentDiskVolumeSource] = None,
        portworx_volume: Optional[PortworxVolumeSource] = None,
        quobyte: Optional[QuobyteVolumeSource] = None,
        rbd: Optional[RBDPersistentVolumeSource] = None,
        scale_io: Optional[ScaleIOPersistentVolumeSource] = None,
        storage_class_name: Optional[str] = None,
        storageos: Optional[StorageOSPersistentVolumeSource] = None,
        volume_mode: Optional[str] = None,
        vsphere_volume: Optional[VsphereVirtualDiskVolumeSource] = None,
    ):
        self.accessModes = access_modes
        self.capacity = capacity
        self.hostPath = host_path
        self.awsElasticBlockStore = aws_elastic_block_store
        self.azureDisk = azure_disk
        self.azureFile = azure_file
        self.cephfs = cephfs
        self.cinder = cinder
        self.claimRef = claim_ref
        self.csi = csi
        self.fc = fc
        self.flexVolume = flex_volume
        self.flocker = flocker
        self.gcePersistentDisk = gce_persistent_disk
        self.glusterfs = glusterfs
        self.iscsi = iscsi
        self.local = local
        self.mountOptions = mount_options
        self.nfs = nfs
        self.nodeAffinity = node_affinity
        self.persistentVolumeReclaimPolicy = persistent_volume_reclaim_policy
        self.photonPersistentDisk = photon_persistent_disk
        self.portworxVolume = portworx_volume
        self.quobyte = quobyte
        self.rbd = rbd
        self.scaleIO = scale_io
        self.storageClassName = storage_class_name
        self.storageos = storageos
        self.volumeMode = volume_mode
        self.vsphereVolume = vsphere_volume


class LoadBalancerIngress(HelmYaml):
    """
    :param hostname:Hostname is set for load-balancer ingress points that are DNS \
        based (typically AWS load-balancers)
    :type hostname: str
    :param ip:IP is set for load-balancer ingress points that are IP based (typically \
        GCE or OpenStack load-balancers)
    :type ip: str
    """

    def __init__(self, hostname: str, ip: str):
        self.hostname = hostname
        self.ip = ip


class Taint(HelmYaml):
    """
    :param effect:Required. The effect of the taint on pods that do not tolerate the \
        taint. Valid effects are NoSchedule, PreferNoSchedule and NoExecute.
    :type effect: str
    :param key:Required. The taint key to be applied to a node.
    :type key: str
    :param time_added:TimeAdded represents the time at which the taint was added. It \
        is only written for NoExecute taints.
    :type time_added: time
    :param value:The taint value corresponding to the taint key.
    :type value: str
    """

    def __init__(self, effect: str, key: str, time_added: time, value: str):
        self.effect = effect
        self.key = key
        self.timeAdded = time_added
        self.value = value


class ConfigMapNodeConfigSource(HelmYaml):
    """
    :param name:Name is the metadata.name of the referenced ConfigMap. This field is \
        required in all cases.
    :type name: str
    :param kubelet_config_key:KubeletConfigKey declares which key of the referenced \
        ConfigMap corresponds to the KubeletConfiguration structure This field is \
        required in all cases.
    :type kubelet_config_key: str
    :param namespace:Namespace is the metadata.namespace of the referenced ConfigMap. \
        This field is required in all cases.
    :type namespace: Optional[str]
    :param resource_version:ResourceVersion is the metadata.ResourceVersion of the \
        referenced ConfigMap. This field is forbidden in Node.Spec, and required in \
        Node.Status.
    :type resource_version: Optional[str]
    :param uid:UID is the metadata.UID of the referenced ConfigMap. This field is \
        forbidden in Node.Spec, and required in Node.Status.
    :type uid: Optional[str]
    """

    def __init__(
        self,
        name: str,
        kubelet_config_key: str,
        namespace: Optional[str] = None,
        resource_version: Optional[str] = None,
        uid: Optional[str] = None,
    ):
        self.name = name
        self.kubeletConfigKey = kubelet_config_key
        self.namespace = namespace
        self.resourceVersion = resource_version
        self.uid = uid


class EndpointPort(HelmYaml):
    """
    :param name:The name of this port.  This must match the 'name' field in the \
        corresponding ServicePort. Must be a DNS_LABEL. Optional only if one port is \
        defined.
    :type name: str
    :param app_protocol:The application protocol for this port. This field follows \
        standard Kubernetes label syntax. Un-prefixed names are reserved for IANA \
        standard service names (as per RFC-6335 and \
        http://www.iana.org/assignments/service-names). Non-standard protocols should \
        use prefixed names such as mycompany.com/my-custom-protocol. Field can be \
        enabled with ServiceAppProtocol feature gate.
    :type app_protocol: str
    :param port:The port number of the endpoint.
    :type port: int
    :param protocol:The IP protocol for this port. Must be UDP, TCP, or SCTP. Default \
        is TCP.
    :type protocol: Optional[str]
    """

    def __init__(
        self, name: str, app_protocol: str, port: int, protocol: Optional[str] = None
    ):
        self.name = name
        self.appProtocol = app_protocol
        self.port = port
        self.protocol = protocol


class EndpointAddress(HelmYaml):
    """
    :param hostname:The Hostname of this endpoint
    :type hostname: str
    :param ip:The IP of this endpoint. May not be loopback (127.0.0.0/8), link-local \
        (169.254.0.0/16), or link-local multicast ((224.0.0.0/24). IPv6 is also \
        accepted but not fully supported on all platforms. Also, certain kubernetes \
        components, like kube-proxy, are not IPv6 ready.
    :type ip: str
    :param node_name:Optional: Node hosting this endpoint. This can be used to \
        determine endpoints local to a node.
    :type node_name: Optional[str]
    :param target_ref:Reference to object providing the endpoint.
    :type target_ref: Optional[ObjectReference]
    """

    def __init__(
        self,
        hostname: str,
        ip: str,
        node_name: Optional[str] = None,
        target_ref: Optional[ObjectReference] = None,
    ):
        self.hostname = hostname
        self.ip = ip
        self.nodeName = node_name
        self.targetRef = target_ref


class EndpointSubset(HelmYaml):
    """
    :param addresses:IP addresses which offer the related ports that are marked as \
        ready. These endpoints should be considered safe for load balancers and \
        clients to utilize.
    :type addresses: List[EndpointAddress]
    :param not_ready_addresses:IP addresses which offer the related ports but are not \
        currently marked as ready because they have not yet finished starting, have \
        recently failed a readiness check, or have recently failed a liveness check.
    :type not_ready_addresses: Optional[List[EndpointAddress]]
    :param ports:Port numbers available on the related IP addresses.
    :type ports: Optional[List[EndpointPort]]
    """

    def __init__(
        self,
        addresses: List[EndpointAddress],
        not_ready_addresses: Optional[List[EndpointAddress]] = None,
        ports: Optional[List[EndpointPort]] = None,
    ):
        self.addresses = addresses
        self.notReadyAddresses = not_ready_addresses
        self.ports = ports


class Endpoints(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param subsets:The set of all endpoints is the union of all subsets. Addresses are \
        placed into subsets according to the IPs they share. A single address with \
        multiple ports, some of which are ready and some of which are not (because \
        they come from different containers) will result in the address being \
        displayed in different subsets for the different ports. No address will appear \
        in both Addresses and NotReadyAddresses in the same subset. Sets of addresses \
        and ports that comprise a service.
    :type subsets: Optional[List[EndpointSubset]]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        subsets: Optional[List[EndpointSubset]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.subsets = subsets


class EventSource(HelmYaml):
    """
    :param component:Component from which the event is generated.
    :type component: str
    :param host:Node name on which the event is generated.
    :type host: str
    """

    def __init__(self, component: str, host: str):
        self.component = component
        self.host = host


class AttachedVolume(HelmYaml):
    """
    :param name:Name of the attached volume
    :type name: str
    :param device_path:DevicePath represents the device path where the volume should \
        be available
    :type device_path: str
    """

    def __init__(self, name: str, device_path: str):
        self.name = name
        self.devicePath = device_path


class NodeCondition(HelmYaml):
    """
    :param last_heartbeat_time:Last time we got an update on a given condition.
    :type last_heartbeat_time: time
    :param last_transition_time:Last time the condition transit from one status to \
        another.
    :type last_transition_time: time
    :param message:Human readable message indicating details about last transition.
    :type message: str
    :param reason:(brief) reason for the condition's last transition.
    :type reason: str
    :param type:Type of node condition.
    :type type: str
    """

    def __init__(
        self,
        last_heartbeat_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastHeartbeatTime = last_heartbeat_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class PodTemplateList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of pod templates
    :type items: List[PodTemplate]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[PodTemplate],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class DaemonEndpoint(HelmYaml):
    """
    :param port:Port number of the given endpoint.
    :type port: int
    """

    def __init__(self, port: int):
        self.Port = port


class NodeDaemonEndpoints(HelmYaml):
    """
    :param kubelet_endpoint:Endpoint on which Kubelet is listening.
    :type kubelet_endpoint: DaemonEndpoint
    """

    def __init__(self, kubelet_endpoint: DaemonEndpoint):
        self.kubeletEndpoint = kubelet_endpoint


class NodeConfigSource(HelmYaml):
    """
    :param config_map:ConfigMap is a reference to a Node's ConfigMap
    :type config_map: ConfigMapNodeConfigSource
    """

    def __init__(self, config_map: ConfigMapNodeConfigSource):
        self.configMap = config_map


class ContainerImage(HelmYaml):
    """
    :param names:Names by which this image is known. e.g. \
        ["k8s.gcr.io/hyperkube:v1.0.7", \
        "dockerhub.io/google_containers/hyperkube:v1.0.7"]
    :type names: List[str]
    :param size_bytes:The size of the image in bytes.
    :type size_bytes: int
    """

    def __init__(self, names: List[str], size_bytes: int):
        self.names = names
        self.sizeBytes = size_bytes


class NodeAddress(HelmYaml):
    """
    :param address:The node address.
    :type address: str
    :param type:Node address type, one of Hostname, ExternalIP or InternalIP.
    :type type: str
    """

    def __init__(self, address: str, type: str):
        self.address = address
        self.type = type


class NodeSystemInfo(HelmYaml):
    """
    :param architecture:The Architecture reported by the node
    :type architecture: str
    :param boot_id:Boot ID reported by the node.
    :type boot_id: str
    :param container_runtime_version:ContainerRuntime Version reported by the node \
        through runtime remote API (e.g. docker://1.5.0).
    :type container_runtime_version: str
    :param kernel_version:Kernel Version reported by the node from 'uname -r' (e.g. \
        3.16.0-0.bpo.4-amd64).
    :type kernel_version: str
    :param kube_proxy_version:KubeProxy Version reported by the node.
    :type kube_proxy_version: str
    :param kubelet_version:Kubelet Version reported by the node.
    :type kubelet_version: str
    :param machine_id:MachineID reported by the node. For unique machine \
        identification in the cluster this field is preferred. Learn more from man(5) \
        machine-id: http://man7.org/linux/man-pages/man5/machine-id.5.html
    :type machine_id: str
    :param operating_system:The Operating System reported by the node
    :type operating_system: str
    :param os_image:OS Image reported by the node from /etc/os-release (e.g. Debian \
        GNU/Linux 7 (wheezy)).
    :type os_image: str
    :param system_uuid:SystemUUID reported by the node. For unique machine \
        identification MachineID is preferred. This field is specific to Red Hat hosts \
        https://access.redhat.com/documentation/en-US/Red_Hat_Subscription_Management/1/html/RHSM/getting-system-uuid.html  # noqa
    :type system_uuid: str
    """

    def __init__(
        self,
        architecture: str,
        boot_id: str,
        container_runtime_version: str,
        kernel_version: str,
        kube_proxy_version: str,
        kubelet_version: str,
        machine_id: str,
        operating_system: str,
        os_image: str,
        system_uuid: str,
    ):
        self.architecture = architecture
        self.bootID = boot_id
        self.containerRuntimeVersion = container_runtime_version
        self.kernelVersion = kernel_version
        self.kubeProxyVersion = kube_proxy_version
        self.kubeletVersion = kubelet_version
        self.machineID = machine_id
        self.operatingSystem = operating_system
        self.osImage = os_image
        self.systemUUID = system_uuid


class NodeSpec(HelmYaml):
    """
    :param external_id:Deprecated. Not all kubelets will set this field. Remove field \
        after 1.13. see: https://issues.k8s.io/61966
    :type external_id: str
    :param pod_cidr:PodCIDR represents the pod IP range assigned to the node.
    :type pod_cidr: str
    :param config_source:If specified, the source to get node configuration from The \
        DynamicKubeletConfig feature gate must be enabled for the Kubelet to use this \
        field
    :type config_source: Optional[NodeConfigSource]
    :param pod_cidrs:podCIDRs represents the IP ranges assigned to the node for usage \
        by Pods on that node. If this field is specified, the 0th entry must match the \
        podCIDR field. It may contain at most 1 value for each of IPv4 and IPv6.
    :type pod_cidrs: Optional[List[str]]
    :param provider_id:ID of the node assigned by the cloud provider in the format: \
        <ProviderName>://<ProviderSpecificNodeID>
    :type provider_id: Optional[str]
    :param taints:If specified, the node's taints.
    :type taints: Optional[List[Taint]]
    :param unschedulable:Unschedulable controls node schedulability of new pods. By \
        default, node is schedulable. More info: \
        https://kubernetes.io/docs/concepts/nodes/node/#manual-node-administration
    :type unschedulable: Optional[bool]
    """

    def __init__(
        self,
        external_id: str,
        pod_cidr: str,
        config_source: Optional[NodeConfigSource] = None,
        pod_cidrs: Optional[List[str]] = None,
        provider_id: Optional[str] = None,
        taints: Optional[List[Taint]] = None,
        unschedulable: Optional[bool] = None,
    ):
        self.externalID = external_id
        self.podCIDR = pod_cidr
        self.configSource = config_source
        self.podCIDRs = pod_cidrs
        self.providerID = provider_id
        self.taints = taints
        self.unschedulable = unschedulable


class Node(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the behavior of a node. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: NodeSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: NodeSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class NodeList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of nodes
    :type items: List[Node]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Node], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class LimitRangeSpec(HelmYaml):
    """
    :param limits:Limits is the list of LimitRangeItem objects that are enforced.
    :type limits: List[LimitRangeItem]
    """

    def __init__(self, limits: List[LimitRangeItem]):
        self.limits = limits


class LimitRange(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the limits enforced. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: LimitRangeSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: LimitRangeSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class LimitRangeList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:Items is a list of LimitRange objects. More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type items: List[LimitRange]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[LimitRange],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class NamespaceCondition(HelmYaml):
    """
    :param last_transition_time:None
    :type last_transition_time: time
    :param message:None
    :type message: str
    :param reason:None
    :type reason: str
    :param type:Type of namespace controller condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class ContainerStateWaiting(HelmYaml):
    """
    :param message:Message regarding why the container is not yet running.
    :type message: str
    :param reason:(brief) reason the container is not yet running.
    :type reason: str
    """

    def __init__(self, message: str, reason: str):
        self.message = message
        self.reason = reason


class ReplicationControllerCondition(HelmYaml):
    """
    :param last_transition_time:The last time the condition transitioned from one \
        status to another.
    :type last_transition_time: time
    :param message:A human readable message indicating details about the transition.
    :type message: str
    :param reason:The reason for the condition's last transition.
    :type reason: str
    :param type:Type of replication controller condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class ContainerStateRunning(HelmYaml):
    """
    :param started_at:Time at which the container was last (re-)started
    :type started_at: time
    """

    def __init__(self, started_at: time):
        self.startedAt = started_at


class ContainerStateTerminated(HelmYaml):
    """
    :param container_id:Container's ID in the format 'docker://<container_id>'
    :type container_id: str
    :param exit_code:Exit status from the last termination of the container
    :type exit_code: int
    :param finished_at:Time at which the container last terminated
    :type finished_at: time
    :param message:Message regarding the last termination of the container
    :type message: str
    :param reason:(brief) reason from the last termination of the container
    :type reason: str
    :param signal:Signal from the last termination of the container
    :type signal: int
    :param started_at:Time at which previous execution of the container started
    :type started_at: time
    """

    def __init__(
        self,
        container_id: str,
        exit_code: int,
        finished_at: time,
        message: str,
        reason: str,
        signal: int,
        started_at: time,
    ):
        self.containerID = container_id
        self.exitCode = exit_code
        self.finishedAt = finished_at
        self.message = message
        self.reason = reason
        self.signal = signal
        self.startedAt = started_at


class ContainerState(HelmYaml):
    """
    :param running:Details about a running container
    :type running: ContainerStateRunning
    :param terminated:Details about a terminated container
    :type terminated: ContainerStateTerminated
    :param waiting:Details about a waiting container
    :type waiting: ContainerStateWaiting
    """

    def __init__(
        self,
        running: ContainerStateRunning,
        terminated: ContainerStateTerminated,
        waiting: ContainerStateWaiting,
    ):
        self.running = running
        self.terminated = terminated
        self.waiting = waiting


class NamespaceSpec(HelmYaml):
    """
    :param finalizers:Finalizers is an opaque list of values that must be empty to \
        permanently remove object from storage. More info: \
        https://kubernetes.io/docs/tasks/administer-cluster/namespaces/
    :type finalizers: Optional[List[str]]
    """

    def __init__(self, finalizers: Optional[List[str]] = None):
        self.finalizers = finalizers


class ServiceAccountList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of ServiceAccounts. More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/  # noqa
    :type items: List[ServiceAccount]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ServiceAccount],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class Namespace(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the behavior of the Namespace. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: Optional[NamespaceSpec]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: Optional[NamespaceSpec] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class NamespaceList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:Items is the list of Namespace objects in the list. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
    :type items: List[Namespace]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[Namespace],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class EndpointsList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of endpoints.
    :type items: List[Endpoints]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[Endpoints],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class EventSeries(HelmYaml):
    """
    :param count:Number of occurrences in this series up to the last heartbeat time
    :type count: int
    :param last_observed_time:Time of the last occurrence observed
    :type last_observed_time: time
    :param state:State of this Series: Ongoing or Finished Deprecated. Planned removal \
        for 1.18
    :type state: str
    """

    def __init__(self, count: int, last_observed_time: time, state: str):
        self.count = count
        self.lastObservedTime = last_observed_time
        self.state = state


class Event(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param involved_object:The object that this event is about.
    :type involved_object: ObjectReference
    :param action:What action was taken/failed regarding to the Regarding object.
    :type action: Optional[str]
    :param count:The number of times this event has occurred.
    :type count: Optional[int]
    :param event_time:Time when this Event was first observed.
    :type event_time: Optional[time]
    :param first_timestamp:The time at which the event was first recorded. (Time of \
        server receipt is in TypeMeta.)
    :type first_timestamp: Optional[time]
    :param last_timestamp:The time at which the most recent occurrence of this event \
        was recorded.
    :type last_timestamp: Optional[time]
    :param message:A human-readable description of the status of this operation.
    :type message: Optional[str]
    :param reason:This should be a short, machine understandable string that gives the \
        reason for the transition into the object's current status.
    :type reason: Optional[str]
    :param related:Optional secondary object for more complex actions.
    :type related: Optional[ObjectReference]
    :param reporting_component:Name of the controller that emitted this Event, e.g. \
        `kubernetes.io/kubelet`.
    :type reporting_component: Optional[str]
    :param reporting_instance:ID of the controller instance, e.g. `kubelet-xyzf`.
    :type reporting_instance: Optional[str]
    :param series:Data about the Event series this event represents or nil if it's a \
        singleton Event.
    :type series: Optional[EventSeries]
    :param source:The component reporting this event. Should be a short machine \
        understandable string.
    :type source: Optional[EventSource]
    :param type:Type of this event (Normal, Warning), new types could be added in the \
        future
    :type type: Optional[str]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        involved_object: ObjectReference,
        action: Optional[str] = None,
        count: Optional[int] = None,
        event_time: Optional[time] = None,
        first_timestamp: Optional[time] = None,
        last_timestamp: Optional[time] = None,
        message: Optional[str] = None,
        reason: Optional[str] = None,
        related: Optional[ObjectReference] = None,
        reporting_component: Optional[str] = None,
        reporting_instance: Optional[str] = None,
        series: Optional[EventSeries] = None,
        source: Optional[EventSource] = None,
        type: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.involvedObject = involved_object
        self.action = action
        self.count = count
        self.eventTime = event_time
        self.firstTimestamp = first_timestamp
        self.lastTimestamp = last_timestamp
        self.message = message
        self.reason = reason
        self.related = related
        self.reportingComponent = reporting_component
        self.reportingInstance = reporting_instance
        self.series = series
        self.source = source
        self.type = type


class EventList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of events
    :type items: List[Event]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Event], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class PodIP(HelmYaml):
    """
    :param ip:ip is an IP address (IPv4 or IPv6) assigned to the pod
    :type ip: str
    """

    def __init__(self, ip: str):
        self.ip = ip


class PodCondition(HelmYaml):
    """
    :param last_probe_time:Last time we probed the condition.
    :type last_probe_time: time
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:Human-readable message indicating details about last transition.
    :type message: str
    :param reason:Unique, one-word, CamelCase reason for the condition's last \
        transition.
    :type reason: str
    :param type:Type is the type of the condition. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions  # noqa
    :type type: str
    """

    def __init__(
        self,
        last_probe_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastProbeTime = last_probe_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class ServicePort(HelmYaml):
    """
    :param port:The port that will be exposed by this service.
    :type port: int
    :param app_protocol:The application protocol for this port. This field follows \
        standard Kubernetes label syntax. Un-prefixed names are reserved for IANA \
        standard service names (as per RFC-6335 and \
        http://www.iana.org/assignments/service-names). Non-standard protocols should \
        use prefixed names such as mycompany.com/my-custom-protocol. Field can be \
        enabled with ServiceAppProtocol feature gate.
    :type app_protocol: Optional[str]
    :param name:The name of this port within the service. This must be a DNS_LABEL. \
        All ports within a ServiceSpec must have unique names. When considering the \
        endpoints for a Service, this must match the 'name' field in the EndpointPort. \
        Optional if only one ServicePort is defined on this service.
    :type name: Optional[str]
    :param node_port:The port on each node on which this service is exposed when \
        type=NodePort or LoadBalancer. Usually assigned by the system. If specified, \
        it will be allocated to the service if unused or else creation of the service \
        will fail. Default is to auto-allocate a port if the ServiceType of this \
        Service requires one. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport  # noqa
    :type node_port: Optional[int]
    :param protocol:The IP protocol for this port. Supports "TCP", "UDP", and "SCTP". \
        Default is TCP.
    :type protocol: Optional[str]
    :param target_port:Number or name of the port to access on the pods targeted by \
        the service. Number must be in the range 1 to 65535. Name must be an \
        IANA_SVC_NAME. If this is a string, it will be looked up as a named port in \
        the target Pod's container ports. If this is not specified, the value of the \
        'port' field is used (an identity map). This field is ignored for services \
        with clusterIP=None, and should be omitted or set equal to the 'port' field. \
        More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service  # noqa
    :type target_port: Optional[int]
    """

    def __init__(
        self,
        port: int,
        app_protocol: Optional[str] = None,
        name: Optional[str] = None,
        node_port: Optional[int] = None,
        protocol: Optional[str] = None,
        target_port: Optional[int] = None,
    ):
        self.port = port
        self.appProtocol = app_protocol
        self.name = name
        self.nodePort = node_port
        self.protocol = protocol
        self.targetPort = target_port


class ServiceSpec(HelmYaml):
    """
    :param ports:The list of ports that are exposed by this service. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type ports: List[ServicePort]
    :param cluster_ip:clusterIP is the IP address of the service and is usually \
        assigned randomly by the master. If an address is specified manually and is \
        not in use by others, it will be allocated to the service; otherwise, creation \
        of the service will fail. This field can not be changed through updates. Valid \
        values are "None", empty string (""), or a valid IP address. "None" can be \
        specified for headless services when proxying is not required. Only applies to \
        types ClusterIP, NodePort, and LoadBalancer. Ignored if type is ExternalName. \
        More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type cluster_ip: Optional[str]
    :param external_ips:externalIPs is a list of IP addresses for which nodes in the \
        cluster will also accept traffic for this service.  These IPs are not managed \
        by Kubernetes.  The user is responsible for ensuring that traffic arrives at a \
        node with this IP.  A common example is external load-balancers that are not \
        part of the Kubernetes system.
    :type external_ips: Optional[List[str]]
    :param external_name:externalName is the external reference that kubedns or \
        equivalent will return as a CNAME record for this service. No proxying will be \
        involved. Must be a valid RFC-1123 hostname \
        (https://tools.ietf.org/html/rfc1123) and requires Type to be ExternalName.
    :type external_name: Optional[str]
    :param external_traffic_policy:externalTrafficPolicy denotes if this Service \
        desires to route external traffic to node-local or cluster-wide endpoints. \
        "Local" preserves the client source IP and avoids a second hop for \
        LoadBalancer and Nodeport type services, but risks potentially imbalanced \
        traffic spreading. "Cluster" obscures the client source IP and may cause a \
        second hop to another node, but should have good overall load-spreading.
    :type external_traffic_policy: Optional[str]
    :param health_check_node_port:healthCheckNodePort specifies the healthcheck \
        nodePort for the service. If not specified, HealthCheckNodePort is created by \
        the service api backend with the allocated nodePort. Will use user-specified \
        nodePort value if specified by the client. Only effects when Type is set to \
        LoadBalancer and ExternalTrafficPolicy is set to Local.
    :type health_check_node_port: Optional[int]
    :param ip_family:ipFamily specifies whether this Service has a preference for a \
        particular IP family (e.g. IPv4 vs. IPv6).  If a specific IP family is \
        requested, the clusterIP field will be allocated from that family, if it is \
        available in the cluster.  If no IP family is requested, the cluster's primary \
        IP family will be used. Other IP fields (loadBalancerIP, \
        loadBalancerSourceRanges, externalIPs) and controllers which allocate external \
        load-balancers should use the same IP family.  Endpoints for this Service will \
        be of this family.  This field is immutable after creation. Assigning a \
        ServiceIPFamily not available in the cluster (e.g. IPv6 in IPv4 only cluster) \
        is an error condition and will fail during clusterIP assignment.
    :type ip_family: Optional[str]
    :param load_balancer_ip:Only applies to Service Type: LoadBalancer LoadBalancer \
        will get created with the IP specified in this field. This feature depends on \
        whether the underlying cloud-provider supports specifying the loadBalancerIP \
        when a load balancer is created. This field will be ignored if the \
        cloud-provider does not support the feature.
    :type load_balancer_ip: Optional[str]
    :param load_balancer_source_ranges:If specified and supported by the platform, \
        this will restrict traffic through the cloud-provider load-balancer will be \
        restricted to the specified client IPs. This field will be ignored if the \
        cloud-provider does not support the feature." More info: \
        https://kubernetes.io/docs/tasks/access-application-cluster/configure-cloud-provider-firewall/  # noqa
    :type load_balancer_source_ranges: Optional[List[str]]
    :param publish_not_ready_addresses:publishNotReadyAddresses, when set to true, \
        indicates that DNS implementations must publish the notReadyAddresses of \
        subsets for the Endpoints associated with the Service. The default value is \
        false. The primary use case for setting this field is to use a StatefulSet's \
        Headless Service to propagate SRV records for its Pods without respect to \
        their readiness for purpose of peer discovery.
    :type publish_not_ready_addresses: Optional[bool]
    :param selector:Route service traffic to pods with label keys and values matching \
        this selector. If empty or not present, the service is assumed to have an \
        external process managing its endpoints, which Kubernetes will not modify. \
        Only applies to types ClusterIP, NodePort, and LoadBalancer. Ignored if type \
        is ExternalName. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/
    :type selector: Optional[dict]
    :param session_affinity:Supports "ClientIP" and "None". Used to maintain session \
        affinity. Enable client IP based session affinity. Must be ClientIP or None. \
        Defaults to None. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type session_affinity: Optional[str]
    :param session_affinity_config:sessionAffinityConfig contains the configurations \
        of session affinity.
    :type session_affinity_config: Optional[SessionAffinityConfig]
    :param topology_keys:topologyKeys is a preference-order list of topology keys \
        which implementations of services should use to preferentially sort endpoints \
        when accessing this Service, it can not be used at the same time as \
        externalTrafficPolicy=Local. Topology keys must be valid label keys and at \
        most 16 keys may be specified. Endpoints are chosen based on the first \
        topology key with available backends. If this field is specified and all \
        entries have no backends that match the topology of the client, the service \
        has no backends for that client and connections should fail. The special value \
        "*" may be used to mean "any topology". This catch-all value, if used, only \
        makes sense as the last value in the list. If this is not specified or empty, \
        no topology constraints will be applied.
    :type topology_keys: Optional[List[str]]
    :param type:type determines how the Service is exposed. Defaults to ClusterIP. \
        Valid options are ExternalName, ClusterIP, NodePort, and LoadBalancer. \
        "ExternalName" maps to the specified externalName. "ClusterIP" allocates a \
        cluster-internal IP address for load-balancing to endpoints. Endpoints are \
        determined by the selector or if that is not specified, by manual construction \
        of an Endpoints object. If clusterIP is "None", no virtual IP is allocated and \
        the endpoints are published as a set of endpoints rather than a stable IP. \
        "NodePort" builds on ClusterIP and allocates a port on every node which routes \
        to the clusterIP. "LoadBalancer" builds on NodePort and creates an external \
        load-balancer (if supported in the current cloud) which routes to the \
        clusterIP. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types  # noqa
    :type type: Optional[str]
    """

    def __init__(
        self,
        ports: List[ServicePort],
        cluster_ip: Optional[str] = None,
        external_ips: Optional[List[str]] = None,
        external_name: Optional[str] = None,
        external_traffic_policy: Optional[str] = None,
        health_check_node_port: Optional[int] = None,
        ip_family: Optional[str] = None,
        load_balancer_ip: Optional[str] = None,
        load_balancer_source_ranges: Optional[List[str]] = None,
        publish_not_ready_addresses: Optional[bool] = None,
        selector: Optional[dict] = None,
        session_affinity: Optional[str] = None,
        session_affinity_config: Optional[SessionAffinityConfig] = None,
        topology_keys: Optional[List[str]] = None,
        type: Optional[str] = None,
    ):
        self.ports = ports
        self.clusterIP = cluster_ip
        self.externalIPs = external_ips
        self.externalName = external_name
        self.externalTrafficPolicy = external_traffic_policy
        self.healthCheckNodePort = health_check_node_port
        self.ipFamily = ip_family
        self.loadBalancerIP = load_balancer_ip
        self.loadBalancerSourceRanges = load_balancer_source_ranges
        self.publishNotReadyAddresses = publish_not_ready_addresses
        self.selector = selector
        self.sessionAffinity = session_affinity
        self.sessionAffinityConfig = session_affinity_config
        self.topologyKeys = topology_keys
        self.type = type


class Service(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the behavior of a service. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ServiceSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: ServiceSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class ServiceList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of services
    :type items: List[Service]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[Service],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ResourceQuotaList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:Items is a list of ResourceQuota objects. More info: \
        https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :type items: List[ResourceQuota]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ResourceQuota],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ConfigMap(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param data:Data contains the configuration data. Each key must consist of \
        alphanumeric characters, '-', '_' or '.'. Values with non-UTF-8 byte sequences \
        must use the BinaryData field. The keys stored in Data must not overlap with \
        the keys in the BinaryData field, this is enforced during validation process.
    :type data: dict
    :param binary_data:BinaryData contains the binary data. Each key must consist of \
        alphanumeric characters, '-', '_' or '.'. BinaryData can contain byte \
        sequences that are not in the UTF-8 range. The keys stored in BinaryData must \
        not overlap with the ones in the Data field, this is enforced during \
        validation process. Using this field will require 1.10+ apiserver and kubelet.
    :type binary_data: Optional[dict]
    :param immutable:Immutable, if set to true, ensures that data stored in the \
        ConfigMap cannot be updated (only object metadata can be modified). If not set \
        to true, the field can be modified at any time. Defaulted to nil. This is an \
        alpha field enabled by ImmutableEphemeralVolumes feature gate.
    :type immutable: Optional[bool]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        data: dict,
        binary_data: Optional[dict] = None,
        immutable: Optional[bool] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.data = data
        self.binaryData = binary_data
        self.immutable = immutable


class Binding(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param target:The target object that you want to bind to the standard object.
    :type target: ObjectReference
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        target: ObjectReference,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.target = target


class ReplicationControllerSpec(HelmYaml):
    """
    :param template:Template is the object that describes the pod that will be created \
        if insufficient replicas are detected. This takes precedence over a \
        TemplateRef. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template  # noqa
    :type template: PodTemplateSpec
    :param selector:Selector is a label query over pods that should match the Replicas \
        count. If Selector is empty, it is defaulted to the labels present on the Pod \
        template. Label keys and values that must match in order to be controlled by \
        this replication controller, if empty defaulted to labels on Pod template. \
        More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: dict
    :param min_ready_seconds:Minimum number of seconds for which a newly created pod \
        should be ready without any of its container crashing, for it to be considered \
        available. Defaults to 0 (pod will be considered available as soon as it is \
        ready)
    :type min_ready_seconds: Optional[int]
    :param replicas:Replicas is the number of desired replicas. This is a pointer to \
        distinguish between explicit zero and unspecified. Defaults to 1. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#what-is-a-replicationcontroller  # noqa
    :type replicas: Optional[int]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        selector: dict,
        min_ready_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
    ):
        self.template = template
        self.selector = selector
        self.minReadySeconds = min_ready_seconds
        self.replicas = replicas


class ReplicationController(KubernetesBaseObject):
    """
    :param metadata:If the Labels of a ReplicationController are empty, they are \
        defaulted to be the same as the Pod(s) that the replication controller \
        manages. Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the specification of the desired behavior of the \
        replication controller. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ReplicationControllerSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: ReplicationControllerSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class Pod(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the pod. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: PodSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: PodSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class Secret(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param data:Data contains the secret data. Each key must consist of alphanumeric \
        characters, '-', '_' or '.'. The serialized form of the secret data is a \
        base64 encoded string, representing the arbitrary (possibly non-string) data \
        value here. Described in https://tools.ietf.org/html/rfc4648#section-4
    :type data: Optional[dict]
    :param immutable:Immutable, if set to true, ensures that data stored in the Secret \
        cannot be updated (only object metadata can be modified). If not set to true, \
        the field can be modified at any time. Defaulted to nil. This is an alpha \
        field enabled by ImmutableEphemeralVolumes feature gate.
    :type immutable: Optional[bool]
    :param string_data:stringData allows specifying non-binary secret data in string \
        form. It is provided as a write-only convenience method. All keys and values \
        are merged into the data field on write, overwriting any existing values. It \
        is never output when reading from the API.
    :type string_data: Optional[dict]
    :param type:Used to facilitate programmatic handling of secret data.
    :type type: Optional[str]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        data: Optional[dict] = None,
        immutable: Optional[bool] = None,
        string_data: Optional[dict] = None,
        type: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.data = data
        self.immutable = immutable
        self.stringData = string_data
        self.type = type


class SecretList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:Items is a list of secret objects. More info: \
        https://kubernetes.io/docs/concepts/configuration/secret
    :type items: List[Secret]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Secret], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ConfigMapList(KubernetesBaseObject):
    """
    :param metadata:More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:Items is the list of ConfigMaps.
    :type items: List[ConfigMap]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ConfigMap],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ReplicationControllerList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of replication controllers. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller  # noqa
    :type items: List[ReplicationController]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ReplicationController],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class PersistentVolume(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines a specification of a persistent volume owned by the \
        cluster. Provisioned by an administrator. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistent-volumes  # noqa
    :type spec: PersistentVolumeSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PersistentVolumeSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class PodList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of pods. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md  # noqa
    :type items: List[Pod]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Pod], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class PersistentVolumeClaimList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:A list of persistent volume claims. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :type items: List[PersistentVolumeClaim]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[PersistentVolumeClaim],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class PersistentVolumeList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of persistent volumes. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes
    :type items: List[PersistentVolume]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[PersistentVolume],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
