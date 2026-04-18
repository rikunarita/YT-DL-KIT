import { useEffect, useState } from 'react'
import { ChevronDown, ChevronUp, HelpCircle } from 'lucide-react'
import { settingsAPI } from '../services/api'
import { useTranslation } from '../i18n'

interface YtDlpParameter {
  name: string
  category: string
  description: string
  type: string
  default_value?: string | number | boolean
  required: boolean
  incompatible_with?: string[]
  depends_on?: Record<string, string>
  ui_control: string
  choices?: string[]
}

interface CategoryParams {
  [key: string]: YtDlpParameter[]
}

export default function AdvancedSettings() {
  const [parameters, setParameters] = useState<YtDlpParameter[]>([])
  const [categoryGroups, setCategoryGroups] = useState<CategoryParams>({})
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['General']))
  const [loading, setLoading] = useState(true)
  const [parameterValues, setParameterValues] = useState<Record<string, any>>({})
  const { t } = useTranslation()

  useEffect(() => {
    fetchParameters()
  }, [])

  const fetchParameters = async () => {
    try {
      const response = await settingsAPI.getYtDlpParameters()
      if (response.data.success && response.data.parameters) {
        const params = response.data.parameters
        setParameters(params)

        const grouped: CategoryParams = {}
        params.forEach((param: YtDlpParameter) => {
          if (!grouped[param.category]) {
            grouped[param.category] = []
          }
          grouped[param.category].push(param)
        })
        setCategoryGroups(grouped)
      }
    } catch (error) {
      console.error('Failed to fetch parameters:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories)
    if (newExpanded.has(category)) {
      newExpanded.delete(category)
    } else {
      newExpanded.add(category)
    }
    setExpandedCategories(newExpanded)
  }

  const handleParameterChange = (paramName: string, value: any) => {
    setParameterValues({ ...parameterValues, [paramName]: value })
  }

  const renderParameterInput = (param: YtDlpParameter) => {
    const value = parameterValues[param.name] ?? param.default_value ?? ''

    if (param.type === 'boolean') {
      return (
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={!!value}
            onChange={(e) => handleParameterChange(param.name, e.target.checked)}
            className="mr-2"
          />
          <span className="text-sm">{param.description}</span>
        </label>
      )
    }

    if (param.choices && param.choices.length > 0) {
      return (
        <select
          value={value}
          onChange={(e) => handleParameterChange(param.name, e.target.value)}
          className="input w-full"
        >
          <option value="">{t('advancedSettings.selectOption')}</option>
          {param.choices.map((choice) => (
            <option key={choice} value={choice}>
              {choice}
            </option>
          ))}
        </select>
      )
    }

    return (
      <input
        type={param.type === 'number' ? 'number' : 'text'}
        value={value}
        onChange={(e) => handleParameterChange(param.name, e.target.value)}
        placeholder={param.default_value?.toString()}
        className="input w-full"
      />
    )
  }

  if (loading) {
    return <div className="text-center py-4">{t('advancedSettings.loading')}</div>
  }

  if (Object.keys(categoryGroups).length === 0) {
    return <div className="text-center py-4 text-slate-500">{t('advancedSettings.noParameters')}</div>
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-slate-600 mb-4">
        {t('advancedSettings.description')}
      </div>

      {Object.entries(categoryGroups).map(([category, params]) => (
        <div key={category} className="border border-slate-200 dark:border-slate-700 rounded-lg">
          <button
            onClick={() => toggleCategory(category)}
            className="w-full p-4 flex items-center justify-between bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition"
          >
            <span className="font-medium">{category}</span>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 bg-slate-200 dark:bg-slate-600 px-2 py-1 rounded">
                {params.length}
              </span>
              {expandedCategories.has(category) ? (
                <ChevronUp size={18} />
              ) : (
                <ChevronDown size={18} />
              )}
            </div>
          </button>

          {expandedCategories.has(category) && (
            <div className="p-4 space-y-4 border-t border-slate-200 dark:border-slate-700">
              {params.map((param: YtDlpParameter) => (
                <div key={param.name} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2 font-medium text-sm">
                      <code className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-xs">
                        --{param.name}
                      </code>
                      {param.required && <span className="text-red-500">*</span>}
                      <div className="group relative">
                        <HelpCircle size={16} className="text-slate-400 cursor-help" />
                        <div className="absolute bottom-full left-0 mb-2 hidden group-hover:block w-64 bg-slate-900 text-white text-xs rounded p-2 z-10">
                          {param.description}
                          {param.depends_on && Object.keys(param.depends_on).length > 0 && (
                            <div className="mt-2 text-yellow-300">
                              ⚠️ {t('advancedSettings.dependsOn')}: {Object.keys(param.depends_on).join(', ')}
                            </div>
                          )}
                          {param.incompatible_with && param.incompatible_with.length > 0 && (
                            <div className="mt-2 text-red-300">
                              ⛔ {t('advancedSettings.incompatibleWith')}: {param.incompatible_with.join(', ')}
                            </div>
                          )}
                        </div>
                      </div>
                    </label>
                  </div>
                  <div className="ml-0">
                    {renderParameterInput(param)}
                  </div>
                  <p className="text-xs text-slate-500">
                    {t('advancedSettings.typeLabel')}: <code className="text-xs">{param.type}</code>
                    {param.default_value !== undefined && (
                      <> | {t('advancedSettings.defaultLabel')}: <code className="text-xs">{String(param.default_value)}</code></>
                    )}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
