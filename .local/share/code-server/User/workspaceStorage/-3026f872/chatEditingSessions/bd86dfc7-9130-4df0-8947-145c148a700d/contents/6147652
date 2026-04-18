import { useState, useCallback } from 'react'
import { settingsAPI } from '../services/api'

interface ParameterMetadata {
  name: string
  category: string
  description: string
  type: string
  default_value?: any
  required: boolean
  incompatible_with?: string[]
  depends_on?: Record<string, string>
  ui_control: string
  choices?: string[]
}

interface ValidationError {
  field: string
  message: string
}

/**
 * フロントエンドパラメータ検証・依存関係処理フック
 * バックエンド ConfigParser と同期
 */
export function useParameterValidation() {
  const [parameters, setParameters] = useState<ParameterMetadata[]>([])
  const [parameterValues, setParameterValues] = useState<Record<string, any>>({})
  const [validationErrors, setValidationErrors] = useState<ValidationError[]>([])
  const [warnings, setWarnings] = useState<ValidationError[]>([])
  const [loading, setLoading] = useState(false)

  // パラメータメタデータを取得
  const fetchParameterMetadata = useCallback(async () => {
    try {
      setLoading(true)
      const response = await settingsAPI.getYtDlpParameters()
      if (response.data.success && response.data.parameters) {
        setParameters(response.data.parameters)
      }
    } catch (error) {
      console.error('Failed to fetch parameter metadata:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  // パラメータ値を検証
  const validateParameter = useCallback(
    (paramName: string, value: any): ValidationError[] => {
      const errors: ValidationError[] = []
      const param = parameters.find((p) => p.name === paramName)

      if (!param) {
        return errors
      }

      // 型チェック
      if (param.type === 'number' && value !== '' && isNaN(Number(value))) {
        errors.push({ field: paramName, message: '数値を入力してください' })
      }

      // 必須チェック
      if (param.required && (value === '' || value === undefined)) {
        errors.push({ field: paramName, message: 'このパラメータは必須です' })
      }

      return errors
    },
    [parameters],
  )

  // 依存関係を自動適用
  const applyDependencies = useCallback(
    (changedParam: string, value: any): Record<string, any> => {
      const newValues = { ...parameterValues, [changedParam]: value }
      const param = parameters.find((p) => p.name === changedParam)

      if (!param || !param.depends_on) {
        return newValues
      }

      // 依存パラメータを自動設定
      Object.entries(param.depends_on).forEach(([depParamName, depValue]) => {
        if (value) {
          newValues[depParamName] = depValue
        }
      })

      return newValues
    },
    [parameters, parameterValues],
  )

  // 互換性をチェック
  const checkIncompatibilities = useCallback(
    (changedParam: string): ValidationError[] => {
      const warnings_list: ValidationError[] = []
      const param = parameters.find((p) => p.name === changedParam)

      if (!param || !param.incompatible_with) {
        return warnings_list
      }

      param.incompatible_with.forEach((incompatParamName) => {
        if (parameterValues[incompatParamName]) {
          warnings_list.push({
            field: changedParam,
            message: `⚠️ ${incompatParamName} と同時に使用できません`,
          })
        }
      })

      return warnings_list
    },
    [parameters, parameterValues],
  )

  // パラメータ値を更新（検証・依存関係処理込み）
  const updateParameter = useCallback(
    (paramName: string, value: any) => {
      // 検証
      const errors = validateParameter(paramName, value)
      if (errors.length > 0) {
        setValidationErrors(errors)
      } else {
        setValidationErrors([])
      }

      // 互換性チェック
      const incompatWarnings = checkIncompatibilities(paramName, value)
      setWarnings(incompatWarnings)

      // 依存関係を自動適用
      const updatedValues = applyDependencies(paramName, value)
      setParameterValues(updatedValues)

      return updatedValues
    },
    [validateParameter, checkIncompatibilities, applyDependencies],
  )

  // バッチで複数パラメータを設定
  const setParametersValues = useCallback((values: Record<string, any>) => {
    setParameterValues(values)
  }, [])

  // バリデーション結果をサマリーで取得
  const getValidationSummary = useCallback(() => {
    return {
      isValid: validationErrors.length === 0,
      errorCount: validationErrors.length,
      warningCount: warnings.length,
      errors: validationErrors,
      warnings: warnings,
    }
  }, [validationErrors, warnings])

  // パラメータ値をリセット
  const resetParameters = useCallback(() => {
    setParameterValues({})
    setValidationErrors([])
    setWarnings([])
  }, [])

  return {
    parameters,
    parameterValues,
    validationErrors,
    warnings,
    loading,
    fetchParameterMetadata,
    updateParameter,
    setParametersValues,
    validateParameter,
    applyDependencies,
    checkIncompatibilities,
    getValidationSummary,
    resetParameters,
  }
}
