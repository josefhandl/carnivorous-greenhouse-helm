{{- define "garden.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "garden.labels" -}}
app.kubernetes.io/name: {{ include "garden.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
