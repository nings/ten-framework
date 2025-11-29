/**
 * AI Court Debate Agent - Main Entry Point
 * 线上法庭智能答辩 AI Agent 系统
 */
package main

import (
	"flag"
	"log"
	"os"

	ten "ten_framework/ten_runtime"
)

type appConfig struct {
	PropertyFilePath string
}

type courtDebateApp struct {
	ten.DefaultApp

	cfg *appConfig
}

func (p *courtDebateApp) OnConfigure(
	tenEnv ten.TenEnv,
) {
	// Using the default property.json if not specified.
	if len(p.cfg.PropertyFilePath) > 0 {
		if b, err := os.ReadFile(p.cfg.PropertyFilePath); err != nil {
			log.Fatalf("Failed to read property file %s, err %v\n", p.cfg.PropertyFilePath, err)
		} else {
			tenEnv.InitPropertyFromJSONBytes(b)
		}
	}

	tenEnv.OnConfigureDone()
}

func startAppBlocking(cfg *appConfig) {
	appInstance, err := ten.NewApp(&courtDebateApp{
		cfg: cfg,
	})
	if err != nil {
		log.Fatalf("Failed to create the app, %v\n", err)
	}

	appInstance.Run(true)
	appInstance.Wait()

	ten.EnsureCleanupWhenProcessExit()
}

func setDefaultLog() {
	log.SetFlags(log.LstdFlags | log.Lmicroseconds)
}

func main() {
	// Set the default log format globally
	setDefaultLog()

	log.Println("==============================================")
	log.Println("AI Court Debate Agent Starting...")
	log.Println("线上法庭智能答辩 AI Agent 系统启动中...")
	log.Println("==============================================")

	cfg := &appConfig{}

	flag.StringVar(&cfg.PropertyFilePath, "property", "", "The absolute path of property.json")
	flag.Parse()

	startAppBlocking(cfg)
}
